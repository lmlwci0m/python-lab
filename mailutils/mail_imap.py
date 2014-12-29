__author__ = 'roberto'

import imaplib


host = 'imap.gmail.com'

M = imaplib.IMAP4_SSL(host, 993)

from_field_email = "xxx@yyy.zzz"

user = "username@email.com"
password = "password"

print(M.login(user, password))
#for box in M.list()[1]:
#    print(box.decode('utf-8'))

#typ, data = M.search(None, 'ALL')
#for num in data[0].split():
#    typ, data = M.fetch(num, '(RFC822)')
#    print('Message %s\n%s\n' % (num, data[0][1]))
#M.close()

print(M.select("INBOX", True))

typ, msgnums = M.search(None, '(FROM "{}")'.format(from_field_email))

#print(typ)
print(msgnums)

msg = M.fetch("14459", '(RFC822)')

for line in msg[1][0]:

    print(line.decode('utf-8'))


print(M.logout())
