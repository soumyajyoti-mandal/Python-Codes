import re
import os

class userActions:
    def __init__(self, option):
        self.userselection = option

#function to check for valid email address
    def registrationemail(self,email):
        pattern = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
        if re.match(pattern,email):
            return True
        else:
            return False

# function verify the conditions of password set is met
    def setpassword(self, password):
        self.keyvalue = password
        if len(self.keyvalue) > 5 and len(self.keyvalue) < 16: #verify length of password
            if re.search('[a-z]',self.keyvalue) and re.search('[A-Z]',self.keyvalue) and re.search('[0-9]',self.keyvalue) and re.search('[@_!#$%^&*()<>?/\|}{~:]', self.keyvalue): #verify minimum required charaters provided
                print("Password Accepted")
                return True
            else:
                print("Password should contain minimum 1 special character, 1 digit, 1 upper case and 1 lowercase character")
                return False
        else:
            print("Password should be within 5 to 16 characters long!")
            return False

# function to save login credentials to file
    def savecredentials(self,email,password): #saving the user entered email and password to text file
        write_file = open("credentials.txt","at")
        write_file.writelines("\n")
        write_file.writelines(email + " " + password)
        print("Credentials saved to credentials.txt file")
        write_file.close()
#function to check if email is present in file
    def verifyemail(self,email):
        eof_flg = False
        match_flag = 0
        if os.path.exists("credentials.txt"):
            read_file = open("credentials.txt", "rt")
            while not eof_flg:
                read_data = read_file.readline()
                if read_data == "":
                    eof_flg = True
                else:
                    user_data_list = read_data.split(" ")
                    if user_data_list[0] == email:
                        match_flag = 1
                        break
        else:
            #print("Credentials file not found!")
            match_flag = 2
        return match_flag
#function to check login credentials
    def userlogin(self,email,password):
        eof_flg = False
        match_flag = 0
        if os.path.exists("credentials.txt"):
            read_file = open("credentials.txt","rt")
            while not eof_flg:
                read_data = read_file.readline()
                if read_data == "":
                    eof_flg = True
                else:
                    user_data_list = read_data.split(" ")
                    if user_data_list[0] == email and user_data_list[1] == password:
                        match_flag = 1
                        break
                    elif user_data_list[0] == email and user_data_list[1] != password:
                        match_flag = 2
                        break
            read_file.close()
            return match_flag
        else:
            no_file = "Credentials file not found"
            return no_file

#function to retrieve forgotten password
    def forgotpassword(self,email):
        eof_flg = False
        match_flag = 0
        if os.path.exists("credentials.txt"):
            read_file = open("credentials.txt", "rt")
            while not eof_flg:
                read_data = read_file.readline()
                if read_data == "":
                    eof_flg = True
                else:
                    user_data_list = read_data.split(" ")
                    if user_data_list[0] == email:
                        match_flag = 1
                        return user_data_list[1]
            if match_flag == 0:
                no_match = "Email not found!"
                return no_match
            read_file.close()
        else:
            no_file = "Credentials file not found"
            return no_file
#function to set new password
    def setnewpassword(self,email):
        eof_flg = False
        match_flag = 0
        if os.path.exists("credentials.txt"):
            read_file = open("credentials.txt", "r")
            while not eof_flg:
                read_data = read_file.readline()
                if read_data == "":
                    eof_flg = True
                else:
                    user_data_list = read_data.split(" ")
                    if user_data_list[0] == email:
                        match_flag = 1
                        verify_password = False
                        while not verify_password:
                            print("Please set a valid password\n")
                            user_password = input()
                            verify_password = self.setpassword(user_password)
            read_file.close()
            #code to rewrite the file with updated password
            if match_flag == 1:
                with open("credentials.txt", 'r') as file:
                    lines = file.readlines()
                file.close()
                with open("credentials.txt", 'w') as file:
                    for line in lines:
                        # find() returns -1 if no match is found
                        if line.find(email) != -1:
                            pass
                        else:
                            file.write(line)
                file.close()
                append_file = open("credentials.txt","a")
                append_file.write("\n"+email +" "+user_password )
                append_file.close()
                print("Password updated successfully")
            else:
                print("Email not found in file!")
        else:
            print("Credentials file not found")

action_complete = 0
action_complete_2 = 0
#loop to get valid selection from user
while action_complete == 0:
    print("Select from the option below")
    print("\n1 - Register \n2 - Login \n3 - Forgot Password \n4 - Exit")
    opt = input()
    if not opt.isnumeric():
        print("Please enter a valid selection")
        continue
    else:
        opt = int(opt)
        uactions = userActions(opt)
        if opt == 1:
            while True:
                print("Please enter a valid email")
                eaddress = input().strip()
                verify_email = uactions.registrationemail(eaddress)
                if verify_email:
                    print("Email is valid")
                    verify_password = False
                    while not verify_password:
                        print("Please set a valid password\n")
                        upassword = input()
                        verify_password = uactions.setpassword(upassword)
                    action_complete = 1
                    uactions.savecredentials(eaddress,upassword)
                    break
                else:
                    print("Email is invalid.")
        elif opt == 2:
            print("Please enter your email:")
            user_email = input().strip()
            print("Please enter password:")
            user_pwd = input().strip()
            check_credentials = uactions.userlogin(user_email,user_pwd) #look for credentials in file
            if check_credentials == 1: #credentials match
                print("Login successful")
                action_complete = 1
            elif check_credentials == 2: #credentials do not match
                print("Credentials does not match. Please verify or select Forgot Password.")
            elif check_credentials == "Credentials file not found":
                action_complete = 1
                print(check_credentials)
            else: #credentials not present in file
                print("Credentials not found. Please select Register!")
        elif opt == 3:
            print("Please enter your email:")
            user_email = input().strip()
            check_email = uactions.verifyemail(user_email)
            if check_email == 0:
                print("Credentials not found. Please select Register!")
            elif check_email == 2:
                print("Credentials file not found!")
                break
            elif check_email == 1:
                # loop to get valid selection from user
                while action_complete_2 == 0:
                    print("Please select from options below:")
                    print("1 - Retrieve password \n2 - Set new password")
                    option = input()
                    if not option.isnumeric():
                        print("Please enter a valid selection:")
                        continue
                    else:
                        option = int(option)
                        if option == 1: #code to retrieve password
                            action_complete = 1
                            action_complete_2 = 1
                            getpassword = uactions.forgotpassword(user_email)
                            if getpassword == "Email not found!" or getpassword == "Credentials file not found":
                                print(getpassword)
                            else:
                                print("Password is:",getpassword)
                        elif option == 2: #code to set new password
                            action_complete = 1
                            action_complete_2 = 1
                            uactions.setnewpassword(user_email)
                        else:
                            print("Selection is invalid!")
        elif opt == 4:
            action_complete = 1
            print("Goodbye!")
        else:
            print("Selection is invalid")