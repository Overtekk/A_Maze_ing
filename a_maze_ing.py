from utils.check_config import check_arg


def main() -> None:
    if not check_arg():
        exit(2)


if __name__ == "__main__":
    main()
