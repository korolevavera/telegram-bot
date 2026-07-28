import os
from dotenv import load_dotenv

load_dotenv()

from bot import app

if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=False)
