from dataclasses import dataclass

@dataclass
class TransferItem:
    fileName: str
    fileSize: int
    retryCount: int
