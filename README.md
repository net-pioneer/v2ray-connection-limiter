
# V2ray Connection Limiter

simple script that checks the number of connections of accounts and ban those who have connected more than the allowed limit.

## Installation:

1. **Install git, python and net-tools**

    Determine on which Linux distribution your system is based on. Most Linux systems (including *Ubuntu*) are Debian-based.


    ### Debian-based linux systems

    [Open a terminal window](https://help.ubuntu.com/community/UsingTheTerminal). Copy & paste the following command into the terminal window and hit `Enter`. You may be prompted to enter your password.

    ```shell
    sudo apt update
    sudo apt upgrade
    sudo apt install git
    sudo apt install python3
    sudo apt install python3-pip
    sudo apt install net-tools
    ```


    ### Red Hat-based linux systems

    Open a terminal. Copy & paste the following command into the terminal window and hit `Enter`. You may be prompted to enter your password.

    ```shell
    sudo yum upgrade
    sudo yum install git
    sudo yum install python3
    sudo yum install python3-pip
    sudo yum install net-tools
    ```

2. **Install Python libraries**
    ```shell
    pip install -r requirements.txt
    ```

3. **Clone this repo**
    ```shell
    git clone https://github.com/kulkapis/v2ray-connection-limiter.git
    ```

4. **Change current working directory**
    ```shell
    cd v2ray-connection-limiter
    ```

5. **Edit config.py file and put your data**

6. **Run the script**

    run it on background with
    ```shell
    nohup python3 main.py &
    ```
    or run it normally with
    ```shell
    python3 main.py
    ```
    or you may use arguments in command line
    ```shell 
    python3 main.py --max-allowed-connections 2 --newuser-check-interval 240 -user-check-interval 30
    ```

## License

[MIT](https://choosealicense.com/licenses/mit/)


## Donate

Good news! If you enjoyed this script you could donate to the first author by donating USDT to the following wallet!

wallet (TRC20): `TBFJ3YirXc7vwwuRNeqhcBcQziB3h9bPbs`
