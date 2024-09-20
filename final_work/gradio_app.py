import gradio as gr
import pickle
import pandas as pd
import os

model_pkl_file = os.path.dirname(os.path.realpath(__file__)) + "/model.pkl"
with open(model_pkl_file, 'rb') as file:  
    model = pickle.load(file)

def render_quality(q):
    if q < 6:
        qw = "низкое"
    elif q >= 8:
        qw = "высокое"
    else:
        qw = "среднее"
    return "Ваше качество сна: " + qw + " [" + str(q[0]) + "]"

def convert_time(time_str):
    hour,minutes = map(int,time_str.split(":"))
    return hour + (minutes / 60.0)

def recomendations(act_lvl, diet, steps, bedtime, duration):
    recs = []
    if act_lvl != "high":
        recs.append("увеличение физической активности")
    if diet != "healthy":
        recs.append("соблюдение диеты")
    if steps < 8000:
        recs.append("больше ходить")
    if convert_time(bedtime) < 12.0:
        recs.append("ложиться спать пораньше")
    if duration < 7:
        recs.append("дольше спать")
    return recs


def sleep_quality_recommendation(act_lvl, diet, steps, bedtime, duration):
    max_sleep_quality = 9.0
    df = pd.DataFrame(
        columns=["Physical Activity Level", "Dietary Habits",  "Daily Steps",  "Duration", "Bedtime"], 
        data=[[act_lvl,diet,steps,duration,bedtime]]
        )
    predicted_quality = model.predict(df)
    recs = recomendations(act_lvl, diet, steps, bedtime, duration)
    if len(recs) > 0:
        impr = 100. - (predicted_quality[0]/max_sleep_quality)*100
        rec = "Рекомендуется: " + ",".join(str(element) for element in recs) + ". Возможно улучшение на " + str(impr) + "%."
    else:
        rec = "У вас хорошее качество сна, так держать"
    return render_quality(predicted_quality), rec

demo = gr.Interface(
    sleep_quality_recommendation,
    [
        gr.Radio(
            ["high", "medium", "low"], value='medium', label="Phiscal Activity Level", info=""
        ),
        gr.Radio(
            ["healthy", "medium", "unhealthy"], value='medium', label="Dietary Habits", info=""
        ),
        gr.Slider(1000, 20000, value=8000, step=1000, label="Daily Steps", info=""),
        gr.Textbox(label="Bedtime", value='23:00', info="hh:mm"),
        gr.Slider(3, 10, value=8, step=1, label="Sleep duration", info="")
    ],
    [
        gr.Textbox(label="Calculated sleep quality", info="Max: 9"),
        gr.Textbox(label="Recommendations")
    ],
    title="Введите параметры"
)

if __name__ == "__main__":
    demo.launch()