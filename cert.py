import os
import sys
import json
from PIL import Image, ImageDraw, ImageFont
import qrcode
from log_ref_in_db import save_ref
import textwrap
from datetime import datetime
from num2words import num2words


class Cert:
    issuing_organization_names = {
        "SB Template": "IEEE SB GEC Palakkad",
        "CS Template": "IEEE CS SBC GEC Palakkad",
        "IAS Template": "IEEE IAS SBC GEC Palakkad",
        "WIE Template": "IEEE WIE AG GEC Palakkad",
        "Excelsior21SB Template": "IEEE SB GEC Palakkad",
        "Excelsior21FROMSB Template": "IEEE SB GEC Palakkad",
        "Excelsior21CS Template": "IEEE CS SBC GEC Palakkad",
        "Excelsior21FROMCS Template": "IEEE CS SBC GEC Palakkad",
        "Excelsior21IAS Template": "IEEE IAS SBC GEC Palakkad",
        "Excelsior21FROMIAS Template": "IEEE IAS SBC GEC Palakkad",
    }
    certificate_titles = {
        "Participants": "Certificate Of Participation",
        "Winners": "Certificate of Achievement",
        "Volunteers": "Volunteer Certificate",
        "Coordinators": "Coordinator Certificate"
    }

    def __init__(self, template_type, recipient_type, event_name, event_start_date, is_winner, template_path):
        self.execution_mode = os.environ.get('EXECUTION_MODE')

        self.template_type = template_type
        self.recipient_type = recipient_type
        self.issuing_organization = self.issuing_organization_names[self.template_type]
        self.certificate_title = self.certificate_titles[self.recipient_type]
        self.event_name = event_name
        self.event_start_date = event_start_date
        self.college_name = None
        self.recipient_name = None
        self.cert_path = None
        self.is_winner = is_winner

        self.template_path = template_path

        json_file = open('./templateProperties.json' if self.execution_mode == 'test' else 'src/scripts/templateProperties.json', 'r')
        template_properties = json.load(json_file)[self.template_type][self.recipient_type]

        '''Configurations'''
        # Coordinates
        self.name_coords = (template_properties["name_coords"]["x"], template_properties["name_coords"]["y"])
        self.college_coords = (template_properties["college_coords"]["x"], )
        self.event_coords = (template_properties["event_coords"]["x"], template_properties["event_coords"]["y"])
        self.issuing_organization_coords = (template_properties["issuing_organization_coords"]["x"], template_properties["issuing_organization_coords"]["y"])
        self.position_coords = None if not self.is_winner else (template_properties["position_coords"]["x"], template_properties["position_coords"]["y"])
        self.qrcode_coords = (template_properties["qrcode_coords"]["x"], template_properties["qrcode_coords"]["y"])
        self.date_coords = (template_properties["date_coords"]["x"], template_properties["date_coords"]["y"])

        # Font Setting
        # color
        self.text_color_name = '#012f31'
        self.text_color_college = '#012f31'
        self.text_color_event = '#707071'
        self.text_color_issuing_organization = '#707071'
        self.text_color_date = '#707070'
        self.text_color_position = '#707071'
        # Face
        self.font_for_name = ImageFont.truetype("./fonts/Philosopher-Bold.ttf" if (self.execution_mode == 'test') else "src/scripts/fonts/Philosopher-Bold.ttf", 85)
#         self.font_for_event = ImageFont.truetype("./fonts/Poppins-Regular-400.ttf" if (self.execution_mode == 'test') else "src/scripts/fonts/Poppins-SemiBold-600.ttf", 70)
        # temperory:
        self.font_for_event = ImageFont.truetype("./fonts/Poppins-Regular-400.ttf" if (self.execution_mode == 'test') else "src/scripts/fonts/Poppins-SemiBold-600.ttf", 58)
        self.font_for_college = ImageFont.truetype("./fonts/Philosopher-Regular.ttf" if (self.execution_mode == 'test') else "src/scripts/fonts/Philosopher-Regular.ttf", 50)
        self.font_for_issuing_organization = ImageFont.truetype("./fonts/Poppins-Regular-400.ttf" if (self.execution_mode == 'test') else "src/scripts/fonts/Poppins-SemiBold-600.ttf", 70)
        self.font_for_date = ImageFont.truetype("./fonts/Philosopher-Regular.ttf" if (self.execution_mode == 'test') else "src/scripts/fonts/Poppins-SemiBold-600.ttf", 70)
        self.font_for_position = ImageFont.truetype("./fonts/Philosopher-Regular.ttf" if (self.execution_mode == 'test') else "src/scripts/fonts/Poppins-SemiBold-600.ttf", 70)

    def create(self, recipient_name, college_name, winner_position, dir_name, event_id, recipient_email):
        print("creating certificate for {}".format(recipient_name))
        sys.stdout.flush()
        self.recipient_name = recipient_name
        self.college_name = college_name

        # creating image
        im = Image.open(self.template_path)
        image = Image.new('RGB', im.size, (255, 255, 255))
        image.paste(im)
        d = ImageDraw.Draw(image)

        # Modified
        # TEST
        # CALCULATING TOTAL HEIGHT FROM NAME AND COLLEGE
        lines = textwrap.wrap(self.recipient_name.title(), width=25)
        total_text_height = 0
        for line in lines[:1 if self.is_winner else 2]:
            width, height = d.textsize(line, self.font_for_name)
            total_text_height += height
        total_text_height += 50
        lines = textwrap.wrap(self.college_name.upper(), width=32)
        for line in lines[:2]:
            width, height = d.textsize(line, self.font_for_college)
            total_text_height += height

        # DRAWING NAME
        lines = textwrap.wrap(recipient_name.upper(), width=25)
        y_text = self.name_coords[1]
        for line in lines[:1 if self.is_winner else 2]:
            width, height = d.textsize(line, self.font_for_name)
            d.text((self.name_coords[0] - width / 2, y_text - total_text_height / 2), line, font=self.font_for_name, fill=self.text_color_name)
            y_text += height

        # DRAWING College
        y_text = y_text + 50
        lines = textwrap.wrap(college_name.upper(), width=32)
        # lines = textwrap.wrap(college_name.upper(), width=42)
        for line in lines[:2]:
            width, height = d.textsize(line, self.font_for_college)
            d.text((self.college_coords[0] - width / 2, y_text - total_text_height / 2), line, font=self.font_for_college,
                   fill=self.text_color_college)
            y_text += height

        # CALCULATING AND DRAWING FOR EVENT NAME
        # lines = textwrap.wrap(self.event_name.upper(), width=32)
        lines = textwrap.wrap(self.event_name.upper(), width=33)
        total_text_height = 0
        for line in lines[:3]:
            width, height = d.textsize(line, self.font_for_event)
            total_text_height += height
        y_text = self.event_coords[1]
        for line in lines[:3]:
            width, height = d.textsize(line, self.font_for_event)
            d.text((self.event_coords[0] - width / 2, y_text - total_text_height / 2), line, font=self.font_for_event, fill=self.text_color_event)
            y_text += height

        # PREPROCESSING, CALCULATING LINE SIZE AND DRAWING ISSUING ORGANIZATION
        if self.template_type in ["Excelsior21FROMCS Template", "Excelsior21FROMIAS Template", "Excelsior21FROMSB Template", "Excelsior21SB Template", "Excelsior21CS Template", "Excelsior21IAS Template"]:
            lines = textwrap.wrap(self.issuing_organization.upper(), width=32)
            total_text_height = 0
            for line in lines[:2]:
                width, height = d.textsize(line, self.font_for_issuing_organization)
                total_text_height += height
            y_text = self.issuing_organization_coords[1]
            for line in lines[:2]:
                width, height = d.textsize(line, self.font_for_issuing_organization)
                d.text((self.issuing_organization_coords[0] - width / 2, y_text - total_text_height / 2), line,
                       font=self.font_for_issuing_organization,
                       fill=self.text_color_event)
                y_text += height

        # PREPROCESSING, CALCULATING LINE SIZE AND DRAWING DATE
        self.event_start_date = self.event_start_date.strip()
        self.event_start_date = self.event_start_date.split()[0]
        date_obj = datetime.strptime(self.event_start_date, '%Y-%m-%d')
        day = num2words(int(datetime.strftime(date_obj, '%d')), to='ordinal_num')
        date_in_words = datetime.strftime(date_obj, '%B, %Y').upper()
        date_in_words = day + " " + date_in_words
        date_line_width, date_line_height = d.textsize(date_in_words, self.font_for_date)
        d.text((self.date_coords[0] - date_line_width / 2, self.date_coords[1] - date_line_height / 2),
               date_in_words, fill=self.text_color_date, font=self.font_for_date)

        # CHECKING IS_WINNER, CALCULATING LINE SIZE AND DRAWING POSITION
        if self.is_winner:
            position_line_width, position_line_height = d.textsize(winner_position.upper(), self.font_for_event)
            d.text((self.position_coords[0] - position_line_width / 2, self.position_coords[1] - position_line_height / 2), winner_position.upper(), fill=self.text_color_position, font=self.font_for_position)

        # Adding reference to db
        cert_ref_id = save_ref(event_id, recipient_email, recipient_name)

        # generating and pasting QR Code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=7,
            border=4,
        )
        # TODO: change QR Data URL given for production
        qr_data = "http://localhost:8000/ref/{}".format(cert_ref_id) if self.execution_mode == 'test' else "https://cv.ieeesbgecpkd.org/ref/{}".format(cert_ref_id)
        qr.add_data(qr_data)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        image.paste(qr_img, self.qrcode_coords)

        # saving image
        cert_save_path = "./generated_certificates/{}/{}".format(dir_name, self.recipient_name + ".pdf") if (self.execution_mode == 'test') else "src/scripts/generated_certificates/{}/{}".format(dir_name, self.recipient_name + ".pdf")
        image.save(cert_save_path)

        self.cert_path = cert_save_path
        return self.cert_path

























# class Cert:
#     issuing_organization_names = {
#         "SB Template": "IEEE SB GEC Palakkad",
#         "CS Template": "IEEE CS SBC GEC Palakkad",
#         "IAS Template": "IEEE IAS SBC GEC Palakkad",
#         "WIE Template": "IEEE WIE AG GEC Palakkad"
#     }
#     certificate_titles = {
#         "Participants": "Certificate Of Participation",
#         "Winners": "Certificate of Achievement",
#         "Volunteers": "Volunteer Certificate",
#         "Coordinators": "Coordinator Certificate"
#     }
#
#     def __init__(self, template_type, recipient_type, event_name, event_start_date, is_winner, template_path):
#         self.execution_mode = os.environ.get('EXECUTION_MODE')
#
#         self.template_type = template_type
#         self.recipient_type = recipient_type
#         self.issuing_organization = self.issuing_organization_names[self.template_type]
#         self.certificate_title = self.certificate_titles[self.recipient_type]
#         self.event_name = event_name
#         self.event_start_date = event_start_date
#         self.college_name = None
#         self.recipient_name = None
#         self.cert_path = None
#         self.is_winner = is_winner
#
#         self.template_path = template_path
#
#         json_file = open('./templateProperties.json' if self.execution_mode == 'test' else 'src/scripts/templateProperties.json', 'r')
#         template_properties = json.load(json_file)[self.template_type][self.recipient_type]
#
#         '''Configurations'''
#         # Coordinates
#         self.name_coords = (template_properties["name_coords"]["x"], template_properties["name_coords"]["y"])
#         self.college_coords = (template_properties["college_coords"]["x"], template_properties["college_coords"]["y"])
#         self.event_coords = (template_properties["event_coords"]["x"], template_properties["event_coords"]["y"])
#         self.position_coords = None if not self.is_winner else (template_properties["position_coords"]["x"], template_properties["position_coords"]["y"])
#         self.qrcode_coords = (template_properties["qrcode_coords"]["x"], template_properties["qrcode_coords"]["y"])
#         self.date_coords = (template_properties["date_coords"]["x"], template_properties["date_coords"]["y"])
#
#         # Font Setting
#         # color
#         self.text_color_name = '#012f31'
#         self.text_color_college = '#012f31'
#         self.text_color_event = '#707070'
#         self.text_color_date = '#012f31'
#         self.text_color_position = '#012f31'
#         # Face
#         self.font_for_name = ImageFont.truetype("./fonts/Philosopher-BoldItalic.ttf" if (self.execution_mode == 'test') else "src/scripts/fonts/Philosopher-BoldItalic.ttf", 75)
#         self.font_for_event = ImageFont.truetype("./fonts/Poppins-Regular-400.ttf" if (self.execution_mode == 'test') else "src/scripts/fonts/Poppins-Regular-400.ttf", 50)
#         self.font_for_college = ImageFont.truetype("./fonts/Philosopher-Regular.ttf" if (self.execution_mode == 'test') else "src/scripts/fonts/Philosopher-Regular.ttf", 50)
#         self.font_for_date = ImageFont.truetype("./fonts/Philosopher-Regular.ttf" if (self.execution_mode == 'test') else "src/scripts/fonts/Philosopher-Regular.ttf", 50)
#         self.font_for_position = ImageFont.truetype("./fonts/Philosopher-Regular.ttf" if (self.execution_mode == 'test') else "src/scripts/fonts/Philosopher-Regular.ttf", 50)
#
#     def create(self, recipient_name, college_name, winner_position, dir_name, event_id, recipient_email):
#         print("creating certificate for {}".format(recipient_name))
#         sys.stdout.flush()
#         self.recipient_name = recipient_name
#         self.college_name = college_name
#
#         # creating image
#         im = Image.open(self.template_path)
#         image = Image.new('RGB', im.size, (255, 255, 255))
#         image.paste(im)
#         d = ImageDraw.Draw(image)
#
#         # TODO Collect event_start_date and winner_position
#
#         # line heights
#         name_line_width, name_line_height = d.textsize(self.recipient_name, self.font_for_name)
#         event_line_width, event_line_height = d.textsize(self.event_name, self.font_for_event)
#         college_name_line_width, college_name_line_height = d.textsize(self.college_name, self.font_for_college)
#         date_line_width, date_line_height = d.textsize(self.event_start_date, self.font_for_date)
#         if self.is_winner:
#             position_line_width, position_line_height = d.textsize(winner_position, self.font_for_event)
#
#         # writing text on image
#         d.text((self.name_coords[0] - name_line_width / 2, self.name_coords[1] - name_line_height / 2), self.recipient_name, fill=self.text_color_name, font=self.font_for_name)
#         d.text((self.event_coords[0] - event_line_width / 2, self.event_coords[1] - event_line_height / 2), self.event_name, fill=self.text_color_event, font=self.font_for_event)
#         d.text((self.college_coords[0] - college_name_line_width / 2, self.college_coords[1] - college_name_line_height / 2), self.college_name, fill=self.text_color_college, font=self.font_for_college)
#         d.text((self.date_coords[0] - date_line_width / 2, self.date_coords[1] - date_line_height / 2), self.event_start_date, fill=self.text_color_date, font=self.font_for_date)
#         if winner_position is not None:
#             d.text((self.position_coords[0] - position_line_width / 2, self.position_coords[1] - position_line_height / 2), winner_position, fill=self.text_color_position, font=self.font_for_position)
#
#         # Adding reference to db
#         cert_ref_id = save_ref(event_id, recipient_email, recipient_name)
#
#         # generating and pasting QR Code
#         qr = qrcode.QRCode(
#             version=1,
#             error_correction=qrcode.constants.ERROR_CORRECT_L,
#             box_size=8,
#             border=4,
#         )
#         # TODO: change QR Data URL given for production
#         qr_data = "https://certvalidator.herokuapp.com/ref/{}".format(cert_ref_id) if self.execution_mode == 'test' else "https://certvalidator.herokuapp.com/ref/{}".format(cert_ref_id)
#         qr.add_data(qr_data)
#         qr.make(fit=True)
#         qr_img = qr.make_image(fill_color="black", back_color="white")
#         image.paste(qr_img, self.qrcode_coords)
#
#         # saving image
#         cert_save_path = "./generated_certificates/{}/{}".format(dir_name, self.recipient_name + ".pdf") if (self.execution_mode == 'test') else "src/scripts/generated_certificates/{}/{}".format(dir_name, self.recipient_name + ".pdf")
#         image.save(cert_save_path)
#
#         self.cert_path = cert_save_path
#         return self.cert_path
