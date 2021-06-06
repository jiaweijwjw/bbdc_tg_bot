USERNAME_INPUT_FIELD = "input.txtbox[type='text'][name='txtNRIC']"
PASSWORD_INPUT_FIELD = "input.txtbox[type='password'][name='txtPassword']"
LOGIN_BTN = "input[type='submit'][name='btnLogin']"
CLASS_2A_RADIO_BTN = "input[type='radio'][name='course'][value='2A|946950|0|G0000']"
SELECT_COURSE_BTN = "input.btn[name='btnSubmit'][type='submit']"
SELECT_COURSE_FORM = "form[action='b-selectCourse.asp'][method='post']"
SIDE_BAR_BOOKING_STATEMENT = "tbody > tr:nth-child(28) > td > a"
BOOKING_STATEMENT_FORM = "form[action='b-default.asp'][name='frmStatement']"
MAIN_FRAME = "frame[name='mainFrame']"
SIDE_FRAME = "frame[name='leftFrame']"
CURRENT_PRACTICAL_TRAINING_BOOKING = "form[name='frmStatement'] > table > tbody > tr:nth-child(5) > td > table > tbody > tr[bgcolor='#FFFFFF'] > td"
SIDE_BAR_PRACTICAL_TRAINING_BOOKING = "tbody > tr:nth-child(14) > td:last-child > a"
PRACTICAL_TRAINING_BOOKING_FORM = (
    "form[action='b-2-pLessonBooking1.asp?blnFailPracTest=True']"
)
PRACTICAL_TRAINING_BOOKING_OPTIONS_COMMON_PARENT = "form[action='b-2-pLessonBooking1.asp?blnFailPracTest=True'] > table > tbody > tr > td > table > tbody > tr"
ALL_MONTHS = "td > table > tbody > tr:last-child > td:first-child > input"
ALL_SESSIONS = "td.txt > input:last-child"
ALL_DAYS = "td.txt > input"
SEARCH_PRACTICAL_TRAINING_SLOTS_BTN = "input[type='button'][name='btnSearch']"
AVAILABLE_PRACTICAL_TRAINING_SLOTS_FORM = (
    "form[action='b-2-pLessonBookingConfirm.asp?class=2A&sub=1.01']"
)
PRACTICAL_TRAINING_SLOTS_TABLE = "form[action='b-2-pLessonBookingConfirm.asp?class=2A&sub=1.01'] > table:nth-child(2) > tbody > tr:nth-child(10) > td > table > tbody"
