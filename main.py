from controller.login_controller import LoginController
import sys
sys.dont_write_bytecode = True


def main():
    login_controller = LoginController()
    login_controller.run()


if __name__ == '__main__':
    main()
