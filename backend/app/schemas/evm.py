from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.evm import Interpretation


class EVMRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    bac: Decimal
    pv: Decimal
    ev: Decimal
    ac: Decimal
    cv: Decimal
    sv: Decimal
    cpi: Decimal | None
    spi: Decimal | None
    eac: Decimal | None
    vac: Decimal | None
    cpi_interpretation: Interpretation | None
    spi_interpretation: Interpretation | None
