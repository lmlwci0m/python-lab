__author__ = 'roberto'

import os
import poplib
from email import parser


def main():

    host = 'pop.gmail.com'
    pop_conn = poplib.POP3_SSL(host)
    username = 'recent:username@email.com'
    print(pop_conn.user(username))
    password = 'password'
    print(pop_conn.pass_(password))

    #for x in pop_conn.list():
    #    print(x)

    #msg = pop_conn.retr(307)

    #for x in msg[1]:
    #    print(x.decode())

    msg_list = pop_conn.list()[1]

    num_messages = len(msg_list)
    print("Number of messages: {}".format(num_messages))

    for x in msg_list:
        msg_num = int(x.decode('utf-8').split(" ")[0])
        msg = pop_conn.top(msg_num, 1)[1]
        for line in msg:
            if line.decode('utf-8').startswith("Subject:"):
                print(line.decode('utf-8'))
                break

    #for i in range(numMessages):

    #    print(pop_conn.top(i+1, 10)[1])

    #print(pop_conn.top(numMessages-1, 10)[1])

    pop_conn.quit()


if __name__ == '__main__':
    main()
