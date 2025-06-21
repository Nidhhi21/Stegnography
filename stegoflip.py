import wave
from tkinter import *
from tkinter import filedialog
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

master = Tk()
canvas = Canvas(master, height=650, width=650)
canvas.pack()
master.title("Audio Steganography")

# File path display frame
frame_mid1 = Frame(master, bg='')
frame_mid1.place(x=20, y=100, height=30, width=300)

label_select_encrypted_audio = Label(master, text='Select Encrypted Audio', font='Verdana 12 bold')
label_select_encrypted_audio.place(x=330, y=60)

# Open file button
open_button = Button(master, text="Open File", command=lambda: [open_file(), get_path()])
open_button.place(x=220, y=140, height=30, width=100)

path_label = Label(frame_mid1, bg='white', font='Verdana 8')
path_label.pack(side=LEFT)

# Email input (not used in logic yet)
recipient_email_textbox = Text(master)
recipient_email_textbox.place(x=20, y=370, width=300, height=20)

# Print entered email (can be removed if not used)
email_address = recipient_email_textbox.get(1.0, "end-1c")
print(email_address)

# Exit button
def prevPage():
    master.destroy()
Button(master, text="Click to Exit Program", command=prevPage).pack(fill=X, expand=TRUE, side=LEFT)

# New frame for second file path
frame_mid1 = Frame(bg='')
frame_mid1.place(x=330, y=100, height=30, width=300)

label_select_audio = Label(text='Select Audio to Encode Message', font='Verdana 12 bold')
label_select_audio.place(x=20, y=60)

path = Label(frame_mid1, font='Verdana 8', bg='white')
path.pack(side=LEFT)

# Decode button
open_button = Button(text="Open File", command=lambda: [decode_file()], )
open_button.place(x=530, y=140, height=30, width=100)

# Open and display selected file path
def open_file():
    file = filedialog.askopenfile(mode='r', filetypes=[("Audio Files", '*.*')])
    if file:
        path_label.configure(text=file.name)

# Send email function
def send_email():
    FROM_ADDRESS = "emin87d@gmail.com"
    TO_ADDRESS = "emin001d@gmail.com"
    body = "https://drive.google.com/file/d/125sbqAHmix_ViFksItedUxaIZyPADU-e/view?usp=share_link"

    msg = MIMEMultipart("mixed")
    msg["Subject"] = "Hidden Audio File"
    msg["From"] = FROM_ADDRESS
    msg["To"] = TO_ADDRESS
    text_part = MIMEText(body)
    msg.attach(text_part)

    part = MIMEApplication(open(get_path(), "rb").read())
    part.add_header("Content-Disposition", "attachment", filename=get_path())
    msg.attach(part)

    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    EMAIL_ADDRESS = "emin87d@gmail.com"
    EMAIL_PASSWORD = "iogeycwivtstasrh"  #  Replace this with a safer method in production

    smtp_client = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    smtp_client.ehlo()
    smtp_client.starttls()
    smtp_client.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    smtp_client.sendmail(FROM_ADDRESS, TO_ADDRESS, msg.as_string())
    smtp_client.quit()

def open_file_decode():
    file = filedialog.askopenfile(mode='r', filetypes=[("Audio Files", '*.*')])
    if file:
        filepath = os.path.abspath(file.name)
        path.configure(text=filepath)
        return file.name


def decode_file():
    fp = open_file_decode()
    text = decode(fp)
    decode_text.configure(text=text)


def get_path():
    return str(path_label["text"])


def display_text():
    txt = text_input.get(1.0, "end-1c")
    return txt


def hide_message():
    encode(get_path(), display_text())

file_path_label = Label(frame_mid1, text=get_path(), font='Verdana 12 bold', bg='white')
file_path_label.pack(side=LEFT)

message_label = Label(master, text='Message to Hide', font='Verdana 12 bold')
message_label.place(x=20, y=180)

text_input = Text(master)
text_input.place(x=20, y=210, width=300, height=150)

send_button = Button(master, text="Encrypt", command=lambda: [hide_message(), show_info(), send_email()])
send_button.place(x=200, y=410, height=30, width=100)


frame_bottom = Frame(master, bg='#FFFFFF')
frame_bottom.place(x=20, y=580)
success_text = Label(frame_bottom, text="", font=('Helvetica 13 bold'))
success_text.pack()

def show_info():
    msg = 'Your operation was successful.'
    success_text.configure(text=msg)

def checkFlip(data, a, b):
    store = data & 12
    if store == 0 and (a == 0 and b == 0):
        return data
    elif store == 4 and (a == 0 and b == 1):
        return data
    elif store == 8 and (a == 1 and b == 0):
        return data
    elif store == 12 and (a == 1 and b == 1):
        return data
    else:
        return data ^ 3


def encode(audio_file, message):
    print("\nEncoding Starts..")
    audio = wave.open(audio_file, mode="rb")
    frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))

    message = message + int(((2 * len(frame_bytes)) - (len(message) * 8 * 8)) / 8) * '#'
    bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8, '0') for i in message])))

    j = 0
    for i in range(0, len(frame_bytes), 2):
        a = bits[i]
        b = bits[i + 1]
        frame_bytes[j] = checkFlip(frame_bytes[j], a, b)
        frame_bytes[j] = frame_bytes[j] & 243  # 11110011
        if a == 0 and b == 1:
            frame_bytes[j] += 4
        elif a == 1 and b == 0:
            frame_bytes[j] += 8
        elif a == 1 and b == 1:
            frame_bytes[j] += 12
        j += 1

    frame_modified = bytes(frame_bytes)
    new_audio = wave.open(audio_file, 'wb')
    new_audio.setparams(audio.getparams())
    new_audio.writeframes(frame_modified)
    new_audio.close()
    audio.close()

# Decoding logic
def decode(audio_file):
    print("\nDecoding Starts..")
    audio = wave.open(audio_file, mode='rb')
    frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))
    extracted = []

    for i in range(len(frame_bytes)):
        frame_bytes[i] = frame_bytes[i] & 12
        if frame_bytes[i] == 0:
            extracted.extend([0, 0])
        elif frame_bytes[i] == 4:
            extracted.extend([0, 1])
        elif frame_bytes[i] == 8:
            extracted.extend([1, 0])
        elif frame_bytes[i] == 12:
            extracted.extend([1, 1])

    string = "".join(chr(int("".join(map(str, extracted[i:i + 8])), 2)) for i in range(0, len(extracted), 8))
    decoded = string.split("###")[0]
    audio.close()
    return decoded

# UI for decoded message display
decode_text_msg = Label(text='Hidden Message Inside Audio', font='Verdana 12 bold')
decode_text_msg.place(x=330, y=180)

decode_frame = Frame(bg='white')
decode_frame.place(x=330, y=210, height=150, width=300)
decode_text = Label(decode_frame, bg='white', wraplength=550)
decode_text.pack(side=LEFT)

master.mainloop()
