--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

SET search_path = public, pg_catalog;

--
-- Name: countries_id_seq; Type: SEQUENCE SET; Schema: public; Owner: greencouriers
--

SELECT pg_catalog.setval('countries_id_seq', 1, false);


--
-- Data for Name: countries; Type: TABLE DATA; Schema: public; Owner: greencouriers
--

COPY countries (id, name, iso, lon, lat, north, south, east, west) FROM stdin;
1132	Afghanistan	AF	\N	\N	\N	\N	\N	\N
1133	Aland Islands	AX	\N	\N	\N	\N	\N	\N
1134	Albania	AL	\N	\N	\N	\N	\N	\N
1135	Algeria	DZ	\N	\N	\N	\N	\N	\N
1136	American Samoa	AS	\N	\N	\N	\N	\N	\N
1137	Andorra	AD	\N	\N	\N	\N	\N	\N
1138	Angola	AO	\N	\N	\N	\N	\N	\N
1139	Anguilla	AI	\N	\N	\N	\N	\N	\N
1140	Antarctica	AQ	\N	\N	\N	\N	\N	\N
1141	Antigua and Barbuda	AG	\N	\N	\N	\N	\N	\N
1142	Argentina	AR	\N	\N	\N	\N	\N	\N
1143	Armenia	AM	\N	\N	\N	\N	\N	\N
1144	Aruba	AW	\N	\N	\N	\N	\N	\N
1145	Australia	AU	\N	\N	\N	\N	\N	\N
1146	Austria	AT	\N	\N	\N	\N	\N	\N
1147	Azerbaijan	AZ	\N	\N	\N	\N	\N	\N
1148	Bahamas	BS	\N	\N	\N	\N	\N	\N
1149	Bahrain	BH	\N	\N	\N	\N	\N	\N
1150	Bangladesh	BD	\N	\N	\N	\N	\N	\N
1151	Barbados	BB	\N	\N	\N	\N	\N	\N
1152	Belarus	BY	\N	\N	\N	\N	\N	\N
1153	Belgium	BE	\N	\N	\N	\N	\N	\N
1154	Belize	BZ	\N	\N	\N	\N	\N	\N
1155	Benin	BJ	\N	\N	\N	\N	\N	\N
1156	Bermuda	BM	\N	\N	\N	\N	\N	\N
1157	Bhutan	BT	\N	\N	\N	\N	\N	\N
1158	Bolivia	BO	\N	\N	\N	\N	\N	\N
1159	Bosnia and Herzegovina	BA	\N	\N	\N	\N	\N	\N
1160	Botswana	BW	\N	\N	\N	\N	\N	\N
1161	Bouvet Island	BV	\N	\N	\N	\N	\N	\N
1162	Brazil	BR	\N	\N	\N	\N	\N	\N
1163	British Indian Ocean Territory	IO	\N	\N	\N	\N	\N	\N
1164	Brunei Darussalam	BN	\N	\N	\N	\N	\N	\N
1165	Bulgaria	BG	\N	\N	\N	\N	\N	\N
1166	Burkina Faso	BF	\N	\N	\N	\N	\N	\N
1167	Burundi	BI	\N	\N	\N	\N	\N	\N
1168	Cambodia	KH	\N	\N	\N	\N	\N	\N
1169	Cameroon	CM	\N	\N	\N	\N	\N	\N
1170	Canada	CA	\N	\N	\N	\N	\N	\N
1171	Cape Verde	CV	\N	\N	\N	\N	\N	\N
1172	Cayman Islands	KY	\N	\N	\N	\N	\N	\N
1173	Central African Republic	CF	\N	\N	\N	\N	\N	\N
1174	Chad	TD	\N	\N	\N	\N	\N	\N
1175	Chile	CL	\N	\N	\N	\N	\N	\N
1176	China	CN	\N	\N	\N	\N	\N	\N
1177	Christmas Island	CX	\N	\N	\N	\N	\N	\N
1178	Cocos (Keeling) Islands	CC	\N	\N	\N	\N	\N	\N
1179	Colombia	CO	\N	\N	\N	\N	\N	\N
1180	Comoros	KM	\N	\N	\N	\N	\N	\N
1181	Congo	CG	\N	\N	\N	\N	\N	\N
1182	Congo, Democratic Republic of the	CD	\N	\N	\N	\N	\N	\N
1183	Cook Islands	CK	\N	\N	\N	\N	\N	\N
1184	Costa Rica	CR	\N	\N	\N	\N	\N	\N
1185	Ivory Coast	CI	\N	\N	\N	\N	\N	\N
1186	Croatia	HR	\N	\N	\N	\N	\N	\N
1187	Cuba	CU	\N	\N	\N	\N	\N	\N
1189	Czech Republic	CZ	\N	\N	\N	\N	\N	\N
1190	Denmark	DK	\N	\N	\N	\N	\N	\N
1191	Djibouti	DJ	\N	\N	\N	\N	\N	\N
1192	Dominica	DM	\N	\N	\N	\N	\N	\N
1193	Dominican Republic	DO	\N	\N	\N	\N	\N	\N
1194	Ecuador	EC	\N	\N	\N	\N	\N	\N
1195	Egypt	EG	\N	\N	\N	\N	\N	\N
1196	El Salvador	SV	\N	\N	\N	\N	\N	\N
1197	Equatorial Guinea	GQ	\N	\N	\N	\N	\N	\N
1198	Eritrea	ER	\N	\N	\N	\N	\N	\N
1199	Estonia	EE	\N	\N	\N	\N	\N	\N
1200	Ethiopia	ET	\N	\N	\N	\N	\N	\N
1201	Falkland Islands (Malvinas)	FK	\N	\N	\N	\N	\N	\N
1202	Faroe Islands	FO	\N	\N	\N	\N	\N	\N
1203	Fiji	FJ	\N	\N	\N	\N	\N	\N
1204	Finland	FI	\N	\N	\N	\N	\N	\N
1206	French Guiana	GF	\N	\N	\N	\N	\N	\N
1207	French Polynesia	PF	\N	\N	\N	\N	\N	\N
1208	French Southern Territories	TF	\N	\N	\N	\N	\N	\N
1209	Gabon	GA	\N	\N	\N	\N	\N	\N
1210	Gambia	GM	\N	\N	\N	\N	\N	\N
1211	Georgia	GE	\N	\N	\N	\N	\N	\N
1213	Ghana	GH	\N	\N	\N	\N	\N	\N
1214	Gibraltar	GI	\N	\N	\N	\N	\N	\N
1215	Greece	GR	\N	\N	\N	\N	\N	\N
1216	Greenland	GL	\N	\N	\N	\N	\N	\N
1217	Grenada	GD	\N	\N	\N	\N	\N	\N
1218	Guadeloupe	GP	\N	\N	\N	\N	\N	\N
1220	Guatemala	GT	\N	\N	\N	\N	\N	\N
1221	Guernsey	GG	\N	\N	\N	\N	\N	\N
1222	Guinea	GN	\N	\N	\N	\N	\N	\N
1223	Guinea-Bissau	GW	\N	\N	\N	\N	\N	\N
1224	Guyana	GY	\N	\N	\N	\N	\N	\N
1225	Haiti	HT	\N	\N	\N	\N	\N	\N
1226	Heard Island and McDonald Islands	HM	\N	\N	\N	\N	\N	\N
1227	Holy See (Vatican City State)	VA	\N	\N	\N	\N	\N	\N
1228	Honduras	HN	\N	\N	\N	\N	\N	\N
1229	Hong Kong	HK	\N	\N	\N	\N	\N	\N
1230	Hungary	HU	\N	\N	\N	\N	\N	\N
1231	Iceland	IS	\N	\N	\N	\N	\N	\N
1232	India	IN	\N	\N	\N	\N	\N	\N
1233	Indonesia	ID	\N	\N	\N	\N	\N	\N
1234	Iran, Islamic Republic of	IR	\N	\N	\N	\N	\N	\N
1235	Iraq	IQ	\N	\N	\N	\N	\N	\N
1236	Ireland	IE	\N	\N	\N	\N	\N	\N
1237	Isle of Man	IM	\N	\N	\N	\N	\N	\N
1240	Jamaica	JM	\N	\N	\N	\N	\N	\N
1241	Japan	JP	\N	\N	\N	\N	\N	\N
1242	Jersey	JE	\N	\N	\N	\N	\N	\N
1243	Jordan	JO	\N	\N	\N	\N	\N	\N
1244	Kazakhstan	KZ	\N	\N	\N	\N	\N	\N
1245	Kenya	KE	\N	\N	\N	\N	\N	\N
1246	Kiribati	KI	\N	\N	\N	\N	\N	\N
1247	Korea, Democratic Peoples Republic of	KP	\N	\N	\N	\N	\N	\N
1248	Korea, Republic of	KR	\N	\N	\N	\N	\N	\N
1249	Kuwait	KW	\N	\N	\N	\N	\N	\N
1250	Kyrgyzstan	KG	\N	\N	\N	\N	\N	\N
1251	Lao Peoples Democratic Republic	LA	\N	\N	\N	\N	\N	\N
1252	Latvia	LV	\N	\N	\N	\N	\N	\N
1253	Lebanon	LB	\N	\N	\N	\N	\N	\N
1254	Lesotho	LS	\N	\N	\N	\N	\N	\N
1255	Liberia	LR	\N	\N	\N	\N	\N	\N
1256	Libyan Arab Jamahiriya	LY	\N	\N	\N	\N	\N	\N
1257	Liechtenstein	LI	\N	\N	\N	\N	\N	\N
1258	Lithuania	LT	\N	\N	\N	\N	\N	\N
1259	Luxembourg	LU	\N	\N	\N	\N	\N	\N
1260	Macao	MO	\N	\N	\N	\N	\N	\N
1261	Macedonia, the former Yugoslav Republic of	MK	\N	\N	\N	\N	\N	\N
1262	Madagascar	MG	\N	\N	\N	\N	\N	\N
1263	Malawi	MW	\N	\N	\N	\N	\N	\N
1264	Malaysia	MY	\N	\N	\N	\N	\N	\N
1265	Maldives	MV	\N	\N	\N	\N	\N	\N
1266	Mali	ML	\N	\N	\N	\N	\N	\N
1267	Malta	MT	\N	\N	\N	\N	\N	\N
1268	Marshall Islands	MH	\N	\N	\N	\N	\N	\N
1269	Martinique	MQ	\N	\N	\N	\N	\N	\N
1270	Mauritania	MR	\N	\N	\N	\N	\N	\N
1271	Mauritius	MU	\N	\N	\N	\N	\N	\N
1272	Mayotte	YT	\N	\N	\N	\N	\N	\N
1273	Mexico	MX	\N	\N	\N	\N	\N	\N
1274	Micronesia, Federated States of	FM	\N	\N	\N	\N	\N	\N
1275	Moldova, Republic of	MD	\N	\N	\N	\N	\N	\N
1276	Monaco	MC	\N	\N	\N	\N	\N	\N
1277	Mongolia	MN	\N	\N	\N	\N	\N	\N
1278	Montenegro	ME	\N	\N	\N	\N	\N	\N
1279	Montserrat	MS	\N	\N	\N	\N	\N	\N
1280	Morocco	MA	\N	\N	\N	\N	\N	\N
1281	Mozambique	MZ	\N	\N	\N	\N	\N	\N
1282	Myanmar	MM	\N	\N	\N	\N	\N	\N
1283	Namibia	NA	\N	\N	\N	\N	\N	\N
1284	Nauru	NR	\N	\N	\N	\N	\N	\N
1285	Nepal	NP	\N	\N	\N	\N	\N	\N
1286	Netherlands	NL	\N	\N	\N	\N	\N	\N
1287	Netherlands Antilles	AN	\N	\N	\N	\N	\N	\N
1288	New Caledonia	NC	\N	\N	\N	\N	\N	\N
1289	New Zealand	NZ	\N	\N	\N	\N	\N	\N
1290	Nicaragua	NI	\N	\N	\N	\N	\N	\N
1238	Israel	IL	34.851612000000003	31.046050999999999	32.261761900000003	29.8146123	36.900562200000003	32.802661800000003
1291	Niger	NE	\N	\N	\N	\N	\N	\N
1292	Nigeria	NG	\N	\N	\N	\N	\N	\N
1293	Niue	NU	\N	\N	\N	\N	\N	\N
1294	Norfolk Island	NF	\N	\N	\N	\N	\N	\N
1295	Northern Mariana Islands	MP	\N	\N	\N	\N	\N	\N
1296	Norway	NO	\N	\N	\N	\N	\N	\N
1297	Oman	OM	\N	\N	\N	\N	\N	\N
1298	Pakistan	PK	\N	\N	\N	\N	\N	\N
1299	Palau	PW	\N	\N	\N	\N	\N	\N
1300	Palestinian Territory, Occupied	PS	\N	\N	\N	\N	\N	\N
1301	Panama	PA	\N	\N	\N	\N	\N	\N
1302	Papua New Guinea	PG	\N	\N	\N	\N	\N	\N
1303	Paraguay	PY	\N	\N	\N	\N	\N	\N
1304	Peru	PE	\N	\N	\N	\N	\N	\N
1305	Philippines	PH	\N	\N	\N	\N	\N	\N
1306	Pitcairn	PN	\N	\N	\N	\N	\N	\N
1307	Poland	PL	\N	\N	\N	\N	\N	\N
1309	Puerto Rico	PR	\N	\N	\N	\N	\N	\N
1310	Qatar	QA	\N	\N	\N	\N	\N	\N
1312	Romania	RO	\N	\N	\N	\N	\N	\N
1314	Rwanda	RW	\N	\N	\N	\N	\N	\N
1315	Saint Barthélemy	BL	\N	\N	\N	\N	\N	\N
1316	Saint Helena	SH	\N	\N	\N	\N	\N	\N
1317	Saint Kitts and Nevis	KN	\N	\N	\N	\N	\N	\N
1318	Saint Lucia	LC	\N	\N	\N	\N	\N	\N
1319	Saint Martin (French part)	MF	\N	\N	\N	\N	\N	\N
1320	Saint Pierre and Miquelon	PM	\N	\N	\N	\N	\N	\N
1321	Saint Vincent and the Grenadines	VC	\N	\N	\N	\N	\N	\N
1322	Samoa	WS	\N	\N	\N	\N	\N	\N
1323	San Marino	SM	\N	\N	\N	\N	\N	\N
1324	Sao Tome and Principe	ST	\N	\N	\N	\N	\N	\N
1325	Saudi Arabia	SA	\N	\N	\N	\N	\N	\N
1326	Senegal	SN	\N	\N	\N	\N	\N	\N
1327	Serbia	RS	\N	\N	\N	\N	\N	\N
1328	Seychelles	SC	\N	\N	\N	\N	\N	\N
1329	Sierra Leone	SL	\N	\N	\N	\N	\N	\N
1330	Singapore	SG	\N	\N	\N	\N	\N	\N
1331	Slovakia	SK	\N	\N	\N	\N	\N	\N
1332	Slovenia	SI	\N	\N	\N	\N	\N	\N
1333	Solomon Islands	SB	\N	\N	\N	\N	\N	\N
1334	Somalia	SO	\N	\N	\N	\N	\N	\N
1335	South Africa	ZA	\N	\N	\N	\N	\N	\N
1336	South Georgia and the South Sandwich Islands	GS	\N	\N	\N	\N	\N	\N
1337	Spain	ES	\N	\N	\N	\N	\N	\N
1338	Sri Lanka	LK	\N	\N	\N	\N	\N	\N
1339	Sudan	SD	\N	\N	\N	\N	\N	\N
1340	Suriname	SR	\N	\N	\N	\N	\N	\N
1341	Svalbard and Jan Mayen	SJ	\N	\N	\N	\N	\N	\N
1342	Swaziland	SZ	\N	\N	\N	\N	\N	\N
1343	Sweden	SE	\N	\N	\N	\N	\N	\N
1344	Switzerland	CH	\N	\N	\N	\N	\N	\N
1345	Syrian Arab Republic	SY	\N	\N	\N	\N	\N	\N
1347	Tajikistan	TJ	\N	\N	\N	\N	\N	\N
1348	Tanzania, United Republic of	TZ	\N	\N	\N	\N	\N	\N
1349	Thailand	TH	\N	\N	\N	\N	\N	\N
1350	Timor-Leste	TL	\N	\N	\N	\N	\N	\N
1351	Togo	TG	\N	\N	\N	\N	\N	\N
1352	Tokelau	TK	\N	\N	\N	\N	\N	\N
1353	Tonga	TO	\N	\N	\N	\N	\N	\N
1354	Trinidad and Tobago	TT	\N	\N	\N	\N	\N	\N
1355	Tunisia	TN	\N	\N	\N	\N	\N	\N
1356	Turkey	TR	\N	\N	\N	\N	\N	\N
1357	Turkmenistan	TM	\N	\N	\N	\N	\N	\N
1358	Turks and Caicos Islands	TC	\N	\N	\N	\N	\N	\N
1359	Tuvalu	TV	\N	\N	\N	\N	\N	\N
1360	Uganda	UG	\N	\N	\N	\N	\N	\N
1361	Ukraine	UA	\N	\N	\N	\N	\N	\N
1362	United Arab Emirates	AE	\N	\N	\N	\N	\N	\N
1363	United Kingdom	GB	\N	\N	\N	\N	\N	\N
1365	United States Minor Outlying Islands	UM	\N	\N	\N	\N	\N	\N
1366	Uruguay	UY	\N	\N	\N	\N	\N	\N
1368	Vanuatu	VU	\N	\N	\N	\N	\N	\N
1369	Venezuela, Bolivarian Republic of	VE	\N	\N	\N	\N	\N	\N
1370	Viet Nam	VN	\N	\N	\N	\N	\N	\N
1371	Virgin Islands, British	VG	\N	\N	\N	\N	\N	\N
1372	Virgin Islands, U.S.	VI	\N	\N	\N	\N	\N	\N
1373	Wallis and Futuna	WF	\N	\N	\N	\N	\N	\N
1374	Western Sahara	EH	\N	\N	\N	\N	\N	\N
1375	Yemen	YE	\N	\N	\N	\N	\N	\N
1376	Zambia	ZM	\N	\N	\N	\N	\N	\N
1377	Zimbabwe	ZW	\N	\N	\N	\N	\N	\N
1212	Germany	DE	10.451525999999999	51.165691000000002	55.056823000000001	47.270127000000002	15.0418536	5.8663565999999996
1308	Portugal	PT	-8.2244539999999997	39.399872000000002	42.154204800000002	36.963065200000003	-6.1902090999999997	-9.5467554999999997
1367	Uzbekistan	UZ	64.585262	41.377490999999999	45.60519	37.184330000000003	73.132271000000003	55.996634999999998
1188	Cyprus	CY	33.429859	35.126412999999999	35.701537999999999	34.563510999999998	34.597918999999997	32.273086999999997
1311	Reunion	RE	\N	\N	\N	\N	\N	\N
1313	Russian Federation	RU	105.31875599999999	61.524009999999997	81.856820400000004	41.186799999999998	-169.65629999999999	19.643335
1239	Italy	IT	12.56738	41.871940000000002	45.9839153	37.4773937	20.763180999999999	4.3715789999999997
1364	United States	US	-95.712890999999999	37.090240000000001	64.736641500000005	-5.7034476999999999	-30.146483199999999	-161.27929879999999
1219	Guam	GU	144.79373100000001	13.444304000000001	13.6178764	13.2706058	145.0498498	144.53761220000001
1346	Taiwan, Province of China	TW	113.260825	23.122294	23.1325553	23.112031999999999	113.2768324	113.2448176
1205	France	FR	2.213749	46.227637999999999	50.038002200000001	42.1331639	10.409549999999999	-5.9820520000000004
\.


--
-- PostgreSQL database dump complete
--

