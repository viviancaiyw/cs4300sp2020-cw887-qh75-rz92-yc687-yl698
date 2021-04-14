import download_reviews
from processing import *

import json
import pathlib
import os
import os.path

info_path = 'info/'

# 0-500
# app_ids = [730, 570, 578080, 440, 271590, 304930, 4000, 230410, 359550, 218620, 252490, 444090, 433850, 105600, 292030, 252950, 346110, 221100, 550, 381210, 227300, 319630, 698780, 301520, 236390, 413150, 620, 275850, 242760, 227940, 49520, 377160, 291550, 264710, 391540, 107410, 238960, 203160, 374320, 222880, 322330, 10, 431960, 250900, 582010, 304050, 239140, 8870, 48700, 365590, 211820, 255710, 251570, 755790, 22380, 244850, 322170, 220, 219740, 504370, 291480, 363970, 232090, 221380, 220240, 550650, 305620, 220200, 218230, 386360, 12210, 219640, 262060, 379720, 282070, 206420, 435150, 346900, 427520, 265930, 219150, 289070, 225540, 391220, 204360, 367520, 306130, 304390, 238460, 383870, 268910, 236850, 20920, 241930, 273110, 281990, 212680, 113200, 582160, 331470, 524220, 223470, 113400, 294100, 1250, 205100, 552520, 394360, 55230, 206440, 438100, 238320, 221910, 286690, 361420, 460930, 359320, 200210, 233450, 8190, 555570, 20900, 231430, 813820, 302830, 379430, 213670, 287700, 253710, 265630, 466240, 200510, 274190, 588430, 239820, 12120, 646570, 287390, 700330, 447040, 223710, 440900, 204300, 219990, 261570, 311690, 346010, 280790, 109600, 242050, 311210, 438740, 242920, 477160, 588650, 316010, 24960, 268500, 611500, 239030, 364360, 674940, 234140, 552500, 834910, 70, 323190, 594650, 200710, 513710, 214950, 644560, 208650, 812140, 236430, 393380, 433340, 270880, 243470, 203770, 414340, 554620, 335300, 107100, 242860, 201810, 444200, 204100, 493340, 237930, 489520, 274170, 104900, 355840, 313120, 298110, 299740, 386180, 246620, 99900, 814380, 630, 236870, 24240, 35450, 629760, 40800, 274940, 289650, 50300, 50130, 22370, 304430, 226700, 214490, 108710, 203140, 518790, 250320, 10090, 457140, 200260, 553640, 374570, 583950, 356190, 838350, 349040, 248820, 632360, 393420, 285900, 387990, 397900, 33230, 581320, 257510, 307780, 17390, 418460, 7670, 312990, 241540, 372000, 594570, 337000, 319510, 8980, 310560, 307690, 108600, 244210, 17410, 48000, 236110, 221640, 282140, 360430, 10180, 883710, 489830, 434570, 582660, 247730, 339800, 387290, 424280, 403640, 552990, 323370, 383080, 380600, 33930, 269210, 335240, 333600, 355180, 779340, 260230, 362890, 447820, 302510, 209000, 516750, 262410, 284160, 431240, 261640, 648800, 207140, 259080, 3590, 384190, 42910, 577800, 110800, 105450, 334230, 247080, 648350, 884660, 389730, 250400, 637650, 24200, 466560, 47890, 248570, 476600, 263280, 221040, 241560, 47870, 674020, 235460, 241600, 35140, 240720, 418370, 644930, 383120, 544920, 620980, 224600, 303210, 253230, 668630, 480490, 22330, 238010, 233130, 389570, 298630, 325610, 406150, 212070, 270550, 8500, 35720, 32370, 645630, 312530, 236090, 447020, 238090, 214560, 57300, 235540, 312660, 232430, 245550, 264200, 233720, 39000, 375230, 206210, 427730, 601510, 323470, 39140, 39210, 394510, 420, 447530, 22300, 414700, 326460, 367500, 420530, 578310, 501300, 736190, 65980, 409710, 244450, 374040, 351640, 657200, 235600, 242720, 570940, 666140, 332310, 233860, 434650, 322500, 9900, 313340, 371660, 809960, 376210, 288160, 555220, 245170, 681660, 17460, 278360, 254700, 804320, 356670, 636480, 314160, 289130, 475150, 24980, 237110, 601150, 233270, 324800, 11020, 257850, 239160, 256290, 530700, 475550, 204450, 460920, 420290, 287290, 313160, 582500, 219890, 24010, 202170, 373420, 548430, 612880, 495890, 220440, 39120, 750920, 394230, 454650, 418340, 266840, 4500, 228380, 201790, 206500, 202970, 485510, 237990, 310950, 489940, 678950, 102500, 211500, 613100, 292730, 474960, 368500, 286160, 47810, 871720, 738060, 214420, 212500, 460790, 41700, 48240, 12110, 365450, 365300, 12200, 459820, 402710, 203290, 563560, 239350, 209650, 10500, 209160, 9200, 428690, 209080, 211400, 302670, 282900, 630100, 638970, 442080, 339610, 584400, 298240, 250760, 859580, 206190, 291650, 384300, 238430, 436520, 301640, 285190, 473690, 389430, 353370, 208580, 444640, 841370, 21690]

# 500-1000
app_ids = [268050, 47780, 224760, 529180, 642250, 955050, 294860, 292120, 22320, 35700, 207230, 332800, 453480, 438040, 311340, 423880, 392110, 70000, 364470, 320300, 7940, 265300, 47410, 391720, 405640, 420110, 12900, 311730, 569480, 602520, 17470, 425580, 242680, 24740, 268420, 418240, 245620, 251060, 242700, 113420, 283640, 8850, 228300, 323850, 744900, 225260, 644570, 560380, 505460, 290080, 223100, 234650, 248390, 637090, 65800, 282800, 504230, 44350, 234630, 351290, 365670, 335670, 12220, 976310, 652980, 621060, 48190, 17300, 223750, 360170, 640820, 212800, 728540, 266510, 493900, 212480, 215280, 488790, 210770, 265550, 34870, 249130, 249050, 290340, 359050, 498240, 386940, 787860, 424840, 226860, 368360, 50620, 34900, 388410, 4760, 237310, 675010, 19900, 337340, 481510, 4920, 234670, 429660, 519190, 411300, 15100, 304030, 683320, 388090, 17500, 730310, 266010, 57690, 261820, 210970, 201870, 367580, 375950, 214340, 473850, 359870, 224480, 204880, 626690, 558100, 233290, 394310, 32470, 272060, 893520, 263980, 365360, 258520, 646910, 448510, 6000, 9480, 341940, 2600, 215080, 533300, 342200, 400910, 208140, 17450, 20500, 599140, 368340, 48720, 6910, 385760, 991780, 428550, 666220, 413410, 45760, 388880, 230290, 253250, 232810, 412830, 942970, 301910, 353380, 246900, 286100, 378648, 449960, 844870, 216150, 443810, 732430, 773951, 430960, 313740, 362960, 244160, 296300, 290300, 287980, 474750, 264140, 386070, 866800, 601430, 535930, 245470, 641990, 360940, 212160, 350080, 394690, 48220, 361800, 17520, 304650, 304240, 270150, 55150, 34030, 311560, 324810, 20510, 108800, 71340, 446800, 6020, 665360, 354140, 590380, 291860, 39150, 248610, 204340, 230050, 297000, 300380, 402570, 337320, 712100, 351970, 327410, 268750, 994280, 403190, 635730, 433950, 298900, 341800, 506610, 508440, 502500, 278080, 589290, 251990, 624090, 215470, 761890, 464060, 427290, 3830, 383980, 218640, 17480, 728880, 392160, 848450, 879160, 287450, 63380, 557600, 70400, 226840, 285920, 237870, 413420, 527230, 451340, 643270, 288470, 221680, 706990, 115320, 242640, 49540, 531640, 462770, 21090, 94400, 548570, 42960, 527430, 253430, 562220, 296470, 633030, 17570, 465520, 333420, 38400, 67370, 532210, 50, 466910, 760060, 397340, 383150, 276810, 218680, 38410, 26800, 409720, 215530, 385770, 535230, 213610, 863550, 227860, 464920, 412020, 329430, 362680, 327890, 396750, 240760, 228280, 238370, 329050, 291410, 496300, 232890, 537180, 469820, 360740, 329110, 392950, 239200, 346120, 319910, 331600, 12100, 258970, 204030, 42700, 250180, 314020, 311310, 470220, 102600, 91700, 317470, 584980, 677620, 352520, 252330, 70300, 295790, 390670, 581630, 104200, 272510, 435030, 235800, 356570, 10150, 280, 503560, 40700, 446020, 397950, 616560, 491950, 232010, 270210, 653530, 460950, 517630, 604450, 368230, 233980, 457330, 745880, 445980, 274920, 564710, 367450, 368370, 570660, 429790, 700030, 435400, 705220, 530620, 255220, 537800, 310080, 424370, 268650, 234080, 690530, 203810, 236370, 611790, 352460, 219830, 65930, 512900, 321300, 363680, 736220, 271240, 246420, 231160, 575640, 486310, 9450, 512540, 274520, 471710, 530330, 552100, 230190, 415200, 568220, 378860, 298050, 627690, 24780, 421020, 723780, 263760, 593600, 823130, 921630, 378370, 939960, 363150, 377840, 410320, 307880, 306020, 333950, 293260, 462930, 673950, 773920, 332070, 418030, 320240, 603850, 316790, 368070, 238210, 637850, 304212, 233610, 222480, 1021950, 222730, 536930, 40100, 303390, 213850, 380840, 567640, 25890, 422970, 222940, 858810, 378649, 2280, 57900, 29800, 766570, 560130, 423230, 788260, 526160, 297130, 221260, 519860, 555160, 224460, 346330, 113020, 851100, 130, 255420, 302380, 362490, 40970, 39510, 794260, 234330, 250620, 492720, 445220, 609320, 362930, 751780, 606150, 305260, 572410, 13520, 235340, 571740, 12140, 499440, 633460, 268130, 300080, 243970, 251150, 257730, 280160, 487120, 635260, 555210, 530890, 375910]


def extract_single_game(app_id):
	print("app_id:", app_id)
	# Download reviews.
	print("Download reviews")
	reviews_dict = download_reviews.get_reviews(app_id)

	# Filter review dict (recommendationid -> review info).
	reviews_dict = filter_reviews_dict(reviews_dict)

	# Look at only 'review' text.
	reviews = [r['review'] for r in reviews_dict.values()]

	# Clean reviews.
	print("Clean reviews")
	reviews = list(map(clean_review, reviews))
	reviews = list(filter(lambda x: x!='', reviews))

	# Tranform reviews.
	print("Transform reviews")
	transformed_reviews = list(map(transform_and_remove_words, reviews))
	transformed_reviews = list(filter(lambda x: x!='', transformed_reviews))

	# Extract keyphrases from original reviews.
	print("Keyphrases")
	keyphrases = extract_keyphrases(reviews)

	# Extract keywords from cleaned reviews.
	print("Keywords")
	keywords = extract_keywords(transformed_reviews)
	print(keywords[:10])
	print(keyphrases[:5])

	return keyphrases, keywords

def write_info(info, app_id):
	pathlib.Path(info_path).mkdir(parents=True, exist_ok=True)
	output_path = info_path+'info_'+str(app_id)+'.json'

	with open(output_path, 'w') as f:
		f.write(json.dumps(info)+'\n')

def write_total(keyphrases, keywords, keyphrases_dict, tfidf_dict, count_dict):
	total = {'keyphrases':keyphrases, 'keywords':keywords}

	output_path = 'keyphrases_and_keywords.json'
	with open(output_path, 'w') as f:
		f.write(json.dumps(total, indent=4)+'\n')

	output_path = 'keyphrases_dict.json'
	with open(output_path, 'w') as f:
		f.write(json.dumps(keyphrases_dict, indent=4)+'\n')

	output_path = 'keywords_tfidf_dict.json'
	with open(output_path, 'w') as f:
		f.write(json.dumps(tfidf_dict, indent=4)+'\n')	

	output_path = 'keywords_count_dict.json'
	with open(output_path, 'w') as f:
		f.write(json.dumps(count_dict, indent=4)+'\n')	

def extract_common():
	all_keywords = list()
	all_keyphrases = list()
	count = 0
	for filename in os.listdir(info_path):
		if filename.endswith('.json'):
			with open(info_path+filename, 'r', encoding='utf8') as in_json_file:
				print("Process file", filename)
				info = json.load(in_json_file)
				all_keywords.append(" ".join(info['keywords']))
				all_keyphrases.extend(info['keyphrases'])

	keyphrases, keywords, keyphrases_dict, tfidf_dict, count_dict = extract_common_keywords_and_phrases(all_keywords, all_keyphrases)
	return keyphrases, keywords, keyphrases_dict, tfidf_dict, count_dict


if __name__ == "__main__":
	# for app_id in app_ids:
	# 	app_id = str(app_id)
	# 	output_path = info_path+'info_'+str(app_id)+'.json'
	# 	if os.path.isfile(output_path):
	# 		print(app_id," exists")
	# 		continue

	# 	keyphrases, keywords = extract_single_game(app_id)
	# 	info = {'app_id':app_id, 'keyphrases':keyphrases, 'keywords': keywords}

	# 	write_info(info, app_id)

	keyphrases, keywords, keyphrases_dict, tfidf_dict, count_dict = extract_common()
	write_total(keyphrases, keywords, keyphrases_dict, tfidf_dict, count_dict)