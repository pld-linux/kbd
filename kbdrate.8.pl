.\" {PTM/PB/0.1/18-05-1999/"zresetuj czêstotliwo¶æ samopowtarzania i opó¼nienia klawiatury"}
.\" Copyright 1992, 1994 Rickard E. Faith (faith@cs.unc.edu)
.\" May be distributed under the GNU General Public License
.\" Updated Wed Jun 22 21:09:43 1994, faith@cs.unc.edu
.TH KBDRATE 8 "22 June 1994" "Linux 1.1.19" "Podrêcznik programisty linuxowego"
.SH NAZWA
kbdrate \- zresetuj czêsto¶æ samopowtarzania i opó¼nienia klawiatury
.SH SK£ADNIA
.B "kbdrate [ \-s ] [ \-r"
czêsto¶æ
.B "] [ \-d"
opó¼nienie
.B ]
.SH OPIS
.B kbdrate
jest u¿ywane do zmiany czêstotliwo¶ci samopowtarzania i opó¼nienia
klawiatury IBM. Opó¼nienie jest ilo¶ci± czasu, przez który klawisz musi byæ
wci¶niêty, nim zacznie siê automatycznie powtarzaæ.

U¿ywanie 
.B kbdrate
bez opcji zresetuje czêstotliwo¶æ na 10,9 znaków na sekundê (cps) i ustawi
opó¼nienie na 250 milisekund (mS). S± to warto¶ci domy¶lne IBM.
.SH OPCJE
.TP
.B \-s
Cicho. Nie drukuj ¿adnych komunikatów.
.TP
.BI \-r " czêsto¶æ"
Zmieñ czêsto¶æ na
.I czêsto¶æ
cps.  Dopuszczalny zasiêg waha siê w zakresie 2.0 do 30.0 cps. Mo¿liwe s±
tylko niektóre warto¶ci, a program sam wybierze te, które s± najbli¿sze
podanej warto¶ci. Mo¿liwe warto¶ci, w znakach na sekundê to:
2.0, 2.1, 2.3, 2.5, 2.7, 3.0, 3.3, 3.7, 4.0, 4.3, 4.6,
5.0, 5.5, 6.0, 6.7, 7.5, 8.0, 8.6, 9.2, 10.0, 10.9, 12.0, 13.3, 15.0, 16.0,
17.1, 18.5, 20.0, 21.8, 24.0, 26.7, 30.0.
.TP
.BI \-d " opó¼nienie"
Zmieñ opó¼nienie na
.I opó¼nienie
milisekund. Dopuszczalny zakres jest od 250 do 1000 mS, lecz jedynymi
dopuszczalnymi warto¶ciami (opartymi na ograniczeniach sprzêtowych) s±:
250mS, 500mS, 750mS i 1000mS.
.SH B£ÊDY
Nie wszystkie klawiatury obs³uguj± wszystkie czêsto¶ci.
.PP
Nie wszystkie czêsto¶ci s± mapowane tak samo.
.PP
Ustawianie czêsto¶æi powtarzania nie dzia³a na klawiaturze Gateway AnyKey.
Jeli kto¶ z t± klawiatur± wie jak programowaæ tê klawiaturê, to niech wy¶le
wiadomo¶æ do faith@cs.unc.edu.
.SH PLIKI
.I /etc/rc.local
.br
.I /dev/port
.SH AUTOR
Rik Faith (faith@cs.unc.edu)
