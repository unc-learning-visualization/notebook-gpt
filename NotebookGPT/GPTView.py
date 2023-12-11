from .GPTModel import GPTModel
import ipywidgets as wg
from IPython.display import clear_output, update_display, display

class GPTView():

    def __init__(self, model: GPTModel) -> None:
        self.model = model
        style = {'description_width': 'initial'}

        self.description = wg.HTML(
            value='<b>Working Code:</b>',
            layout=wg.Layout(width='50%'),
            style=style,
            disabled=True
        )

        self.gpt_header = wg.HTML(
            value='<b>ChatGPT Response:</b>',
            layout=wg.Layout(width='50%'),
            style=style,
            disabled=True
        )

        self.current_code = wg.Textarea(
            value='This cell will populate with your history.',
            description='',
            layout=wg.Layout(width='100%', height='200px'),
            continous_update=True,
            style=style,
            disabled=True
        )

        self.gpt_response_code = wg.Textarea(
            value='Hello from ChatGPT!',
            description='',
            layout=wg.Layout(width='50%', height='200px'),
            continous_update=True,
            style=style,
            disabled=True
        )

        self.gpt_insert = wg.HTML(
            value='<b>Ask ChatGPT:</b>',
            layout=wg.Layout(width='50%'),
            style=style,
            disabled=True
        )

        self.gpt_enter_code = wg.Textarea(
            value='Type whatever you like to ChatGPT here!',
            description='',
            layout=wg.Layout(width='50%', height='200px'),
            continous_update=True,
            style=style,
            disabled=False
        )

        self.code = wg.Button(
            description='',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Click to fill your code history to send to ChatGPT.',
            layout=wg.Layout(width='10%'),
            icon='fa-code' # (FontAwesome names without the `fa-` prefix)
        )
        self.code.on_click(self.codeButton)

        self.problem = wg.Button(
            description='',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Click to fill the problem into GPT box with prompt.',
            layout=wg.Layout(width='10%'),
            icon='fa-question-circle' # (FontAwesome names without the `fa-` prefix)
        )
        self.problem.on_click(self.promptButton)

        self.send_gpt = wg.Button(
            description='',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Click to send your message to ChatGPT.',
            layout=wg.Layout(width='10%'),
            icon='fa-comments' # (FontAwesome names without the `fa-` prefix)
        )
        self.send_gpt.on_click(self.sendGPT)

        self.box_0 = wg.HBox([self.description])
        self.box_1 = wg.HBox([self.current_code], layout=wg.Layout(width='100%'))
        self.box_2 = wg.HBox([self.gpt_insert, self.gpt_header])
        self.box_3 = wg.HBox([self.gpt_enter_code, self.gpt_response_code])
        self.box_4 = wg.HBox([self.code, self.problem, self.send_gpt])

    def displayWidget(self):
        display(self.box_0, self.box_1, self.box_2, self.box_3, self.box_4)

    def codeButton(self, click):
        self.model.generateHistoryPrompt()

    def promptButton(self, click):
        self.model.generateProblemPrompt()

    def sendGPT(self, click):
        self.model.sendToGPT(self.gpt_enter_code.value)

    def update(self, event: dict):
        if event['event'] == "Sent_GPT":
            self.gpt_response_code.value = event['value']
        if event['event'] == "History_GPT" or event['event'] == "Problem_GPT":
            self.gpt_enter_code.value = event['value']
        if event['event'] == "Loading":
            self.gpt_response_code.value = event['value']
        if event['event'] == "History_Response":
            if len(event['value']) > 0:
                self.current_code.value = event['value'][0]
        