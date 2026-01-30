import argparse


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Multi-format file parser (CSV, JSON, XML)"
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to the input file"
    )

    args = parser.parse_args()
    print(f"Input file received: {args.input}")


if __name__ == "__main__":
    main()
