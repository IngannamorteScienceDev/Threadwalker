import os
import pandas as pd

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_FILE = os.path.join(BASE_DIR, "data", "processed", "messages_with_roles.csv")
A_FILE = os.path.join(BASE_DIR, "data", "processed", "author_a.csv")
B_FILE = os.path.join(BASE_DIR, "data", "processed", "author_b.csv")


def main():
    df = pd.read_csv(INPUT_FILE)

    if "author_role" not in df.columns:
        print("Missing column 'author_role'. Please run add_author_role.py first.")
        return

    df_a = df[df["author_role"] == "author_a"].copy()
    df_b = df[df["author_role"] == "author_b"].copy()

    df_a.to_csv(A_FILE, index=False, encoding="utf-8")
    df_b.to_csv(B_FILE, index=False, encoding="utf-8")

    print(f"Messages from author_a saved to {A_FILE} ({len(df_a)} messages)")
    print(f"Messages from author_b saved to {B_FILE} ({len(df_b)} messages)")


if __name__ == "__main__":
    main()
