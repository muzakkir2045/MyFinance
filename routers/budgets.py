
import models
from typing import Annotated
from schemas import BudgetCreate, BudgetResponse, BudgetUpdate
from fastapi import status, Depends, HTTPException, APIRouter
from sqlalchemy import select
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from auth import CurrentUser

router = APIRouter()


# Budget Endpoints
# to be deleted
@router.get("/", response_model=list[BudgetResponse])
async def get_budgets(current_user: CurrentUser, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(
        select(models.Budgets).where(models.Budgets.user_id == current_user.id)
    )

    budgets = result.scalars().all()
    return budgets


@router.get("/{budget_id}", response_model=BudgetResponse)
async def get_budget(budget_id: int, current_user: CurrentUser, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(
        select(models.Budgets).where(models.Budgets.id == budget_id, models.Budgets.user_id == current_user.id)
    )

    budget = result.scalars().first()

    if not budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Budget not found"
        )
    return budget



@router.post("/", response_model=BudgetResponse, status_code=status.HTTP_201_CREATED)
async def add_budget(budget:BudgetCreate, current_user: CurrentUser, db: Annotated[AsyncSession, Depends(get_db)]):


    result = await db.execute(
        select(models.Categories.type).where(models.Categories.id == budget.category_id , models.Categories.user_id == current_user.id)
    )
    cat = result.scalars().first()
    if cat == "Income":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Budgets can only be created for expense categories."
        )

    new_budget = models.Budgets(
        category_id = budget.category_id,
        amount = budget.amount,
        user_id = current_user.id
    )

    db.add(new_budget)
    await db.commit()
    await db.refresh(new_budget)

    return new_budget


@router.put("/full/{budget_id}/update", response_model=BudgetResponse)
async def budget_update_full(budget_id:int, current_user: CurrentUser, budget_data: BudgetCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(
        select(models.Budgets).where(models.Budgets.id == budget_id, models.Budgets.user_id == current_user.id)
    )

    budget = result.scalars().first()

    if not budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Budget not found"
        )
    
    budget.category_id = budget_data.category_id
    budget.amount = budget_data.amount

    await db.commit()
    await db.refresh(budget)
    return budget


@router.patch("/partial/{budget_id}/update", response_model=BudgetResponse)
async def budget_update_partial(budget_id:int, current_user: CurrentUser, budget_data: BudgetUpdate, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(
        select(models.Budgets).where(models.Budgets.id == budget_id, models.Budgets.user_id == current_user.id)
    )

    budget = result.scalars().first()

    if not budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Budget not found"
        )
    
    update_data = budget_data.model_dump(exclude_unset=True)

    for field,value in update_data.items():
        setattr(budget, field, value)

    await db.commit()
    await db.refresh(budget)
    return budget


@router.delete("/delete/{budget_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_budget(budget_id:int, current_user: CurrentUser, db:Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(
        select(models.Budgets).where(models.Budgets.id == budget_id, models.Budgets.user_id == current_user.id)
    )

    budget = result.scalars().first()

    if not budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Budget not found"
        )
    
    await db.delete(budget)
    await db.commit()