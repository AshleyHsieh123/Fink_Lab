import gspread
import pandas as pd
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from google.colab import auth, drive
from gspread_dataframe import set_with_dataframe
from google.auth import default
from IPython.display import display, Javascript
from google.colab import output

# Authenticate and mount
drive.mount('/content/drive')
auth.authenticate_user()
creds, _ = default()
gc = gspread.authorize(creds)

# Your actual Google Sheet
file_id = '17t6CB6Nze274z1od3cmfdKnHZ2OMLdFFay7yMQ_Ofi0'
sh = gc.open_by_key(file_id)
worksheet = sh.sheet1

# JS: Create input + plot box
def create_input_box():
    display(Javascript('''
        if (!document.getElementById('customContainer')) {
            const container = document.createElement('div');
            container.id = 'customContainer';

            const input = document.createElement('input');
            input.id = 'myInput';
            input.placeholder = 'Enter a number';
            input.style.margin = '10px';

            const button = document.createElement('button');
            button.textContent = 'Submit';
            button.style.margin = '10px';
            button.onclick = () => {
                const val = document.getElementById('myInput').value;
                google.colab.kernel.invokeFunction("notebook.submit_value", [val], {});
            };

            const plotBox = document.createElement('div');
            plotBox.id = 'plotBox1';
            plotBox.style.marginTop = '20px';

            container.appendChild(input);
            container.appendChild(button);
            container.appendChild(plotBox);
            document.body.appendChild(container);
        }
    '''))

def submit_value(val):
    print(f"📥 Submitted value: {val}")

    try:
        # Update cell A1 in your sheet
        worksheet.update('A1', val)

        # Plot something using the value
        fig, ax = plt.subplots()
        y = [int(val) + i for i in range(3)]
        ax.plot([1, 2, 3], y, marker='o')
        ax.set_title(f"Plot for value = {val}")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")

        # Convert to base64 and embed
        buf = BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()
        plt.close(fig)

        display(Javascript(f'''
            const plotBox = document.getElementById("plotBox1");
            if (plotBox) {{
                plotBox.innerHTML = '<img src="data:image/png;base64,{img_base64}" />';
            }} else {{
                console.log("plotBox1 not found");
            }}
        '''))

    except Exception as e:
        print("❌ Error:", e)

# Register callback
output.register_callback('notebook.submit_value', submit_value)

create_input_box()

