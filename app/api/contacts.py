from fastapi import APIRouter, Depends, status, HTTPException
from app.core.dependencies import get_current_workspace
from app.schemas.contacts import ContactCreate, ContactUpdate, ContactResponse

from app.services.contact_service import (
    create_contact,
    get_contacts,
    update_contact,
    delete_contact
)

router = APIRouter(
    prefix="/api/contacts",
    tags=["Contacts"]
)


@router.post(
    "/",
    response_model=ContactResponse,
    status_code=status.HTTP_201_CREATED
)
def add_contact(
    data: ContactCreate,
    workspace_id: int = Depends(get_current_workspace)
):
    return create_contact(data, workspace_id)


@router.get("/", response_model=list[ContactResponse])
def list_contacts(
    workspace_id: int = Depends(get_current_workspace)
):
    return get_contacts(workspace_id)
@router.put("/{contact_id}", response_model=ContactResponse)
def edit_contact(
    contact_id: int,
    data: ContactUpdate,
    workspace_id: int = Depends(get_current_workspace)
):
    contact = update_contact(contact_id, workspace_id, data)

    if contact is None:
        raise HTTPException(
            status_code=404,
            detail="Contact not found."
        )

    return contact


@router.delete("/{contact_id}")
def remove_contact(
    contact_id: int,
    workspace_id: int = Depends(get_current_workspace)
):
    deleted = delete_contact(contact_id, workspace_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Contact not found."
        )

    return {"message": "Contact deleted successfully."}
