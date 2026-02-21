from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.db.models.sale import Sale
from app.schemas.sale import SaleStageUpdate, SaleOut
from app.models.enums import SalesStage
from app.services.sales_state_machine import SalesStateMachine

router = APIRouter(prefix="/sales", tags=["Sales"])

@router.get("/", response_model=list[SaleOut])
async def get_sales(session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(Sale))
    sales = result.scalars().all() 
    return sales

@router.patch("/{sale_id}/stage", response_model=SaleOut)
async def update_stage(
    sale_id: int,
    data: SaleStageUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Sale).where(Sale.id == sale_id))
    sale = result.scalar_one_or_none()

    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")

    if sale.stage in [SalesStage.paid, SalesStage.lost]:
        raise HTTPException(
            status_code=400,
            detail="Final stage cannot be changed"
        )

    try:
        SalesStateMachine.validate_transition(sale.stage, data.stage)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    sale.stage = data.stage

    await db.commit()
    await db.refresh(sale)

    return SaleOut.model_validate(sale)