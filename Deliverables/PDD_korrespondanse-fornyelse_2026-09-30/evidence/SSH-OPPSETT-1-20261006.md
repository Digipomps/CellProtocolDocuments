== les-ssh-oppsett: 2026-10-06T17:28:04Z ==
-- ssh på denne Macen: OpenSSH_10.3p1, LibreSSL 3.3.6
-- ~/.ssh/config finnes (13 linjer). Innholdet vises ikke.
-- ops
   controlmaster          false
   controlpersist         no
   serveraliveinterval    10
   serveralivecountmax    3
   tcpkeepalive           yes
   connecttimeout         15
   connectionattempts     1
   batchmode              yes
   identitiesonly         yes
   requesttty             auto
   proxyjump              (ikke satt)
   proxycommand           (ikke satt)
   controlpath            (ikke satt)
   ok  hvert kall til ops er sin egen forbindelse
-- root
   controlmaster          false
   controlpersist         no
   serveraliveinterval    10
   serveralivecountmax    3
   tcpkeepalive           yes
   connecttimeout         15
   connectionattempts     1
   batchmode              yes
   identitiesonly         yes
   requesttty             auto
   proxyjump              (ikke satt)
   proxycommand           (ikke satt)
   controlpath            (ikke satt)
   ok  hvert kall til root er sin egen forbindelse
EGNE FORBINDELSER: hvert kall fra bytt-invitasjoner.sh er sin egen forbindelse på denne Macen.
Ingen maskin er kontaktet, og ingenting er endret.
