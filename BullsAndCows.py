import random


class BullsAndCows:
    """
    A class to play the Bulls and Cows game.
    Bulls represent correct digits in the correct positions.
    Cows represent correct digits in the wrong positions.
    """

    def __init__(self, secret=None):
        """
        Initialize the game with an optional secret number.
        If no secret is provided, a random 4-digit number will be generated.
        :type secret: str, optional
        """
        self.secret = secret
        self.guesses = []
        self.hints = []

    def set_secret(self, secret):
        """
        Set the secret number for the game.
        :type secret: str
        """
        self.secret = secret
        self.guesses = []
        self.hints = []

    def get_hint(self, guess):
        """
        Get the hint for a guess compared to the secret.
        :type guess: str
        :rtype: str
        """
        if self.secret is None:
            raise ValueError(
                "Secret number is not set. Please set a secret number first.")

        if len(guess) != len(self.secret):
            raise ValueError(
                f"Guess length ({len(guess)}) must match secret length ({len(self.secret)})"
            )

        secret_dict = {}
        guess_dict = {}

        A = 0  # Bulls: correct digits in correct positions
        B = 0  # Cows: correct digits in wrong positions

        for i in range(len(self.secret)):
            if self.secret[i] == guess[i]:
                A += 1
            else:
                # Count occurrences in secret (excluding bulls)
                if self.secret[i] in secret_dict:
                    secret_dict[
                        self.secret[i]] = secret_dict[self.secret[i]] + 1
                else:
                    secret_dict[self.secret[i]] = 1

                # Count occurrences in guess (excluding bulls)
                if guess[i] in guess_dict:
                    guess_dict[guess[i]] = guess_dict[guess[i]] + 1
                else:
                    guess_dict[guess[i]] = 1

        # Calculate cows (correct digits in wrong positions)
        for digit in secret_dict:
            if digit in guess_dict:
                B += min(secret_dict[digit], guess_dict[digit])

        # Store the guess and hint
        self.guesses.append(guess)
        self.hints.append(str(A) + "A" + str(B) + "B")

        return str(A) + "A" + str(B) + "B"

    def play_round(self, guess):
        """
        Play a round by making a guess and returning the hint.
        Also checks if the guess is correct.
        :type guess: str
        :rtype: tuple (hint: str, is_correct: bool)
        """
        hint = self.get_hint(guess)
        is_correct = hint == f"{len(self.secret)}A0B"
        return hint, is_correct

    def get_game_history(self):
        """
        Get the history of guesses and hints.
        :rtype: list of tuples (guess: str, hint: str)
        """
        return list(zip(self.guesses, self.hints))

    def reset_game(self):
        """
        Reset the game by clearing guesses and hints.
        """
        self.guesses = []
        self.hints = []

    def generate_random_secret(self, length=4):
        """
        Generate a random secret number with the specified length.
        :type length: int
        :rtype: str
        """
        digits = [str(i) for i in range(10)]
        random.shuffle(digits)
        return ''.join(digits[:length])


# Keep the original function for backward compatibility
def getHint(secret, guess):
    """
    :type secret: str
    :type guess: str
    :rtype: str
    """
    secret_dict = {}
    guess_dict = {}

    A = 0
    B = 0
    for i in range(len(secret)):
        if secret[i] == guess[i]:
            A += 1
        else:
            if secret[i] in secret_dict:
                secret_dict[secret[i]] = secret_dict[secret[i]] + 1
            else:
                secret_dict[secret[i]] = 1
            if guess[i] in guess_dict:
                guess_dict[guess[i]] = guess_dict[guess[i]] + 1
            else:
                guess_dict[guess[i]] = 1
    for digit in secret_dict:
        if digit in guess_dict:
            B += min(secret_dict[digit], guess_dict[digit])
    return str(A) + "A" + str(B) + "B"


def play_interactive_game():
    """
    交互式猜数字游戏
    用户可以每次输入一个猜测，电脑验证并给出提示
    """
    print("=== 猜数字游戏 (Bulls and Cows) ===")
    print("规则说明:")
    print("- Bulls (A): 数字正确且位置正确")
    print("- Cows (B): 数字正确但位置错误")
    print("- 例如: 秘密数字是1234，猜测是1357，结果是1A1B")
    print()

    # 选择游戏模式
    print("请选择游戏模式:")
    print("1. 电脑随机生成秘密数字")
    print("2. 手动设置秘密数字")

    while True:
        try:
            mode = input("请输入选择 (1 或 2): ").strip()
            if mode == "1":
                # 随机生成秘密数字
                length = input("请输入数字长度 (默认4): ").strip()
                if not length:
                    length = 4
                else:
                    length = int(length)
                game = BullsAndCows()
                secret = game.generate_random_secret(length)
                game.set_secret(secret)
                print(f"电脑已生成一个{length}位数字，开始游戏!")
                break
            elif mode == "2":
                # 手动设置秘密数字
                secret = input("请输入秘密数字: ").strip()
                if not secret.isdigit():
                    print("错误: 秘密数字必须全部是数字!")
                    continue
                game = BullsAndCows(secret)
                print("秘密数字已设置，开始游戏!")
                break
            else:
                print("无效选择，请输入 1 或 2")
        except ValueError as e:
            print(f"输入错误: {e}")
        except Exception as e:
            print(f"发生错误: {e}")

    print(f"\n秘密数字是{len(game.secret)}位数，开始猜测!")
    print("输入 'quit' 退出游戏，输入 'history' 查看历史记录")
    print("-" * 40)

    attempts = 0
    max_attempts = 10

    while attempts < max_attempts:
        try:
            guess = input(
                f"第{attempts + 1}次猜测 (还剩{max_attempts - attempts}次): ").strip(
                )

            # 处理特殊命令
            if guess.lower() == 'quit':
                print(f"游戏结束。秘密数字是: {game.secret}")
                break
            elif guess.lower() == 'history':
                history = game.get_game_history()
                if history:
                    print("历史记录:")
                    for i, (g, h) in enumerate(history, 1):
                        print(f"  {i}. {g} -> {h}")
                else:
                    print("暂无历史记录")
                continue
            elif guess.lower() == 'help':
                print("可用命令:")
                print("  quit - 退出游戏")
                print("  history - 查看历史记录")
                print("  help - 显示帮助")
                continue

            # 验证输入
            if not guess.isdigit():
                print("错误: 猜测必须全部是数字!")
                continue

            if len(guess) != len(game.secret):
                print(f"错误: 猜测长度必须为{len(game.secret)}位!")
                continue

            # 进行猜测
            hint, is_correct = game.play_round(guess)
            attempts += 1

            print(f"结果: {hint}")

            if is_correct:
                print(f"🎉 恭喜你！在第{attempts}次猜中了秘密数字: {game.secret}")
                break
            else:
                print("继续努力!")

            print("-" * 30)

        except KeyboardInterrupt:
            print(f"\n游戏中断。秘密数字是: {game.secret}")
            break
        except Exception as e:
            print(f"发生错误: {e}")

    if attempts >= max_attempts and not game.play_round(game.guesses[-1])[1]:
        print(f"游戏结束！你已用完{max_attempts}次机会。")
        print(f"秘密数字是: {game.secret}")

    # 显示最终统计
    print("\n游戏统计:")
    print(f"总尝试次数: {attempts}")
    history = game.get_game_history()
    if history:
        print("详细记录:")
        for i, (g, h) in enumerate(history, 1):
            print(f"  {i}. {g} -> {h}")


if __name__ == "__main__":
    play_interactive_game()
