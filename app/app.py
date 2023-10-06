import socket
import random
import os
from flask import Flask
from flask import render_template, url_for

import argparse

app = Flask(__name__)

color_codes = {
    "red": "#e74c3c",
    "green": "#16a085",
    "blue": "#2980b9",
    "ansiblue": "#64C5C7",
    "pink": "#be2edd",
    "darkblue": "#130f40"
}

SUPPORTED_COLORS = ",".join(color_codes.keys())

# Get color from Environment variable
COLOR_FROM_ENV = os.environ.get('APP_COLOR')
IMAGE_FROM_ENV = os.environ.get('APP_IMAGE') or str("https://github.com/ansible/instruqt/blob/main/assets/ansible-demo.png?raw=true")
GITREF_FROM_ENV = os.environ.get('GITREF') or str("not specified")
PUSHER_FROM_ENV = os.environ.get('PUSHER') or str("not specified")
HOSTPORT_FROM_ENV = os.environ.get('HOSTPORT') or str("8080")
# Generate a random color
COLOR = random.choice(["red", "green", "blue", "ansiblue", "darkblue", "pink"])


@app.route("/")
def main():
    # return 'Hello'
    return render_template('hello.html', name=socket.gethostname(), hostport=HOSTPORT_FROM_ENV, color=color_codes[COLOR], pusher=PUSHER_FROM_ENV, gitref=GITREF_FROM_ENV, image=IMAGE_FROM_ENV)


if __name__ == "__main__":

    print(" This is a sample web application that displays a colored background. \n"
          " A color can be specified in two ways. \n"
          "\n"
          " 1. As a command line argument with --color as the argument. Accepts one of " + SUPPORTED_COLORS + " \n"
          " 2. As an Environment variable APP_COLOR. Accepts one of " + SUPPORTED_COLORS + " \n"
          " 3. If none of the above then a random color is picked from the above list. \n"
          " Note: Command line argument precedes over environment variable.\n"
          "\n"
          "")

    # Check for Command Line Parameters for color
    parser = argparse.ArgumentParser()
    parser.add_argument('--color', required=False)
    args = parser.parse_args()

    if args.color:
        print("Color from command line argument =" + args.color)
        COLOR = args.color
        if COLOR_FROM_ENV:
            print("A color was set through environment variable -" + COLOR_FROM_ENV + ". However, color from command line argument takes precendence.")
    elif COLOR_FROM_ENV:
        print("No Command line argument. Color from environment variable =" + COLOR_FROM_ENV)
        COLOR = COLOR_FROM_ENV
    else:
        print("No command line argument or environment variable. Picking a Random Color =" + COLOR)

    # Check if input color is a supported one
    if COLOR not in color_codes:
        print("Color not supported. Received '" + COLOR + "' expected one of " + SUPPORTED_COLORS)
        exit(1)

    # Run Flask Application
    app.run(host="0.0.0.0", port=8080)
