from nanoleafapi import Nanoleaf, RED, ORANGE, YELLOW, GREEN, LIGHT_BLUE, BLUE, PINK, PURPLE, WHITE

import openai

# Setzen Sie den OpenAI API-Schlüssel
openai.api_key = 'YOUR_OPENAI_KEY'

nl=Nanoleaf("YOUR_NANOLEAF_IP")
nl.power_on()
nl.set_color((255,0,0))

# Initialwerte setzen
Licht = None
Farbe = None
Helligkeit = None

# Farben als Tupel definieren
farben = {"RED": RED, "ORANGE": ORANGE, "YELLOW": YELLOW, "GREEN": GREEN, "LIGHT_BLUE": LIGHT_BLUE, "BLUE": BLUE, "PINK": PINK, "PURPLE": PURPLE, "WHITE": WHITE}

def checkvar():
    if Licht:
        nl.power_on()
    elif Licht == False:
        nl.power_off()

    if Farbe in farben:
        nl.set_color(farben[Farbe])
        
    if Helligkeit is not None:
        nl.set_brightness(Helligkeit)

def text_to_var():
    global Licht, Farbe, Helligkeit
    if "(licht=True)" in res:
        Licht=True
    if  "(licht=False)" in res:
        Licht=False
    for farbe in farben:
        if f"(Farbe={farbe})" in res:
            Farbe=farbe
    if "(Helligkeit=" in res:
        helligkeitswert = int(res.split('(Helligkeit=')[1].split(')')[0])
        if 0 <= helligkeitswert <= 100:
            Helligkeit = helligkeitswert

def gbt():
    default_daily_context =  """
    Dilly ist ein KI-gesteuerter Chatbot, der speziell entwickelt wurde, um mit der Nanoleaf-Beleuchtung im Haus zu interagieren. Sie kann die Lichter ein- und ausschalten, ihre Farben ändern und die Helligkeit einstellen. Dilly versteht die Befehle "Licht an", "Licht aus", "Farbe ändern" und "Helligkeit einstellen". Wenn das Licht eingeschaltet ist, ist der Status 'licht=True', und wenn das Licht ausgeschaltet ist, ist der Status 'licht=False'. 

    Bei einer Anfrage zur Farbänderung wird Dilly entweder direkt die gewünschte Farbe einstellen, wenn sie angegeben wird, oder den Benutzer nach der gewünschten Farbe fragen. Die verfügbaren Farben sind RED, ORANGE, YELLOW, GREEN, LIGHT_BLUE, BLUE, PINK, PURPLE und WHITE. Bei einer Anfrage zur Helligkeitsänderung wird Dilly entweder direkt den gewünschten Helligkeitswert einstellen, wenn er angegeben wird, oder den Benutzer nach dem gewünschten Helligkeitswert fragen.

    Beispielinteraktionen:
    1. Benutzer: "Dilly, kannst du das Licht einschalten?"
    Dilly: "Natürlich, ich schalte das Licht ein." (licht=True)
    
    2. Benutzer: "Dilly, kannst du das Licht ausschalten?"
    Dilly: "Sicher, ich schalte das Licht aus." (licht=False)
    
    3. Benutzer: "Dilly, kannst du die Farbe ändern?"
    Dilly: "Natürlich, welche Farbe hätten Sie gerne?"
    
    4. Benutzer: "Dilly, kannst du die Farbe auf BLAU ändern?"
    Dilly: "Sicher, ich ändere die Farbe auf BLAU." (Farbe=BLUE)
    
    5. Benutzer: "Dilly, kannst du die Helligkeit auf 50 ändern?"
    Dilly: "Sicher, ich stelle die Helligkeit auf 50 ein." (Helligkeit=50)
    """

    message =input("Hier Ihre Frage einfügen: ")

    messages = [
        {"role": "system", "content": default_daily_context},
        {"role": "user", "content": message}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=100,
        n=1,
        temperature=0.7,
    )
    global res
    res = response.choices[0].message['content']
    user_friendly_res = res

    # Überprüfen und Entfernen der technischen Details am Ende der Antwort
    technical_details = ['(licht=True)', '(licht=False)'] + [f'(Farbe={farbe})' for farbe in farben] + [f'(Helligkeit={i})' for i in range(101)]
    for var in technical_details:
        if var in user_friendly_res:
            user_friendly_res = user_friendly_res.replace(var, '').strip()

    print(f"Dilly's Antwort: {user_friendly_res}")
    text_to_var()

while True:
    checkvar()
    gbt()
