
import datetime

now = datetime.datetime.now()
current_time = now.strftime("%H:%M:%S")
print(f'''
<div style="font-family: 'Roboto', sans-serif; background: linear-gradient(135deg, #1a1a2e, #16213e); padding: 30px; border-radius: 15px; text-align: center; color: white; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);">
  <h2 style="margin-bottom: 20px; font-size: 2.5em; letter-spacing: 2px; text-shadow: 2px 2px 5px rgba(0,0,0,0.3);">Current Time</h2>
  <div style="font-size: 4em; font-weight: bold; text-shadow: 3px 3px 8px rgba(0,0,0,0.4); animation: pulse 1.5s infinite alternate;">
    {current_time}
  </div>
  <style>
    @keyframes pulse {{
      from {{ transform: scale(1); opacity: 1; }}
      to {{ transform: scale(1.05); opacity: 0.9; }}
    }}
  </style>
</div>
''')
