from fastapi import HTTPException, status


def handle_database_error(e: Exception, custom_conflict_msg: str = "Registro já existe."):
    if isinstance(e, HTTPException):
        raise e

    error_msg = str(e).lower()

    if "unique" in error_msg or "duplicate key" in error_msg or "23505" in error_msg:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=custom_conflict_msg,
        )

    if "foreign key" in error_msg or "23503" in error_msg or "is not present in table" in error_msg:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="O registro relacionado (paciente, prontuário, profissional ou medicamento) não existe.",
        )

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Erro interno no servidor: {str(e)}",
    )