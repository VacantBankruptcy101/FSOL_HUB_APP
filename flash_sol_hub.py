import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from solana.rpc.api import Client
from solana.keypair import Keypair
from spl.token.client import Token
from spl.token.constants import TOKEN_PROGRAM_ID

class FlashSOLHub(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

        self.solana_client = Client("https://api.devnet.solana.com") # Devnet
        self.keypair = Keypair.from_secret_key("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjcmVhdGVkQXQiOjE3NTExNjEyNjU5MDUsImVtYWlsIjoiZWJpei5hbnlsMi4wQGdtYWlsLmNvbSIsImFjdGlvbiI6InRva2VuLWFwaSIsImFwaVZlcnNpb24iOiJ2MiIsImlhdCI6MTc1MTE2MTI2NX0.nR5A8953NajOVESNdGYtPOa3U9uKdKFoDjZ2OVXW9Qw")

    def initUI(self):
        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle('Flash SOL Hub')

        layout = QVBoxLayout()

        label = QLabel("Flash SOL Generator")
        layout.addWidget(label)

        label = QLabel("Recipient Address:")
        layout.addWidget(label)
        self.recipient = QLineEdit()
        layout.addWidget(self.recipient)

        label = QLabel("Amount (FSOL):")
        layout.addWidget(label)
        self.amount = QLineEdit()
        layout.addWidget(self.amount)

        button = QPushButton("Generate Flash SOL")
        button.clicked.connect(self.generate)
        layout.addWidget(button)

        self.status = QLabel("Ready...")
        layout.addWidget(self.status)

        self.setLayout(layout)

    def generate(self):
        recipient = self.recipient.text()
        amount = int(self.amount.text()) * 10**9 # 9 decimals

        try:
            token = Token(
                conn=self.solana_client,
                pubkey="0x5B38Da6a701c568545dCfcB03FcB875f56beddC4",
                program_id=TOKEN_PROGRAM_ID,
                payer=self.keypair,
            )
            tx = token.transfer(
                source=self.keypair.public_key,
                dest=recipient,
                amount=amount,
                opts={"skip_preflight": False, "skip_confirmation": False},
            )
            self.solana_client.send_transaction(tx, self.keypair)
            self.status.setText(f"Sent {amount / 10**9} FSOL to {recipient}!")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = FlashSOLHub()
    ex.show()
    sys.exit(app.exec_())
