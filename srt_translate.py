# -*- coding: utf-8 -*-
import http.client, urllib.parse, uuid, json # must use python 3
import re

# This is what I used for the API information, and where a lot of this code comes from.
# https://docs.microsoft.com/en-us/azure/cognitive-services/translator/quickstart-python-transliterate
# Here is a link to the relevant GitHub page which can also be found in the link above.
# Please refer to this link for licensing information for the API.
# https://github.com/MicrosoftTranslator?type=&language=python

# To use this you'll need:
# - Python 3.x
# - An Azure subscription key for Translator Text

# To get a subscription key for the API you can sign up here:
# https://docs.microsoft.com/en-us/azure/cognitive-services/translator/translator-text-how-to-signup
# At the time of writing, it will let any user translate 
# up to 2 million characters a month for free, and there's no expiration date

# This is a list of language codes and names:
# http://www.emreakkas.com/internationalization/microsoft-translator-api-languages-list-language-codes-and-names
# Could easily put all these codes into a dictionary.

host = 'api.cognitive.microsofttranslator.com'
path = '/translate?api-version=3.0'
# I'm assuming the above wont change, keep them in here for now.

# There are a million ways in which these routines and this package can be
# made more sophisticated. I've only cobbled these functions together so they 
# can produce a reasonable srt file quickly. 

# All this assumes a common srt file format, if you find an srt file that fails to translate
# properly using this, please email me and I'll work on extending this to be more robust.
# This hasn't been extensively tested. Again, if you find a language or script for which
# this fails, please email me.

# Please feel free to email with any other suggestions!

def microsoft_translate(subscriptionKey, params, content):
	# contacts the API to do the translating. Taken almost directly from a tutorial.
	headers = {'Ocp-Apim-Subscription-Key': subscriptionKey, 'Content-type': 'application/json', 'X-ClientTraceId': str(uuid.uuid4())}
	conn = http.client.HTTPSConnection(host)
	conn.request("POST", path + params, content, headers)
	response = conn.getresponse()
	return response.read()


def translate_and_parse(subscriptionKey, params, text):
	# give it text in one language, return text in another language.
	# uses the above function
	requestBody = [{'Text' : text}]
	content = json.dumps(requestBody, ensure_ascii=False).encode('utf-8')
	result = microsoft_translate(subscriptionKey, params, content) #json object
	output = json.loads(result.decode()) # load json object
	# The "decode" isn't in the tutorial. Without it I get an error and
	# googling said error led me to this fix.
	answer = output[0]['translations'][0]['text']
	return answer


def convert_srt_file(inputfile, outputfile, subscriptionKey, tolang, fromlang=None):
	# translate your "inputfile" from one language, 
	# to an "outputfile" in a different language.
	# tolang: Language to translate to
	# fromlang: Optional, language to translate from. The API will autodetect 
			# if this isn't present.
	
	infile = open(inputfile, "r")
	outfile = open(outputfile,"w")
	lines = infile.readlines()

	params="&to="+tolang # language to translate to
	if (fromlang is not None):
		params = "&from=" + fromlang + params

	for line in lines:
		if ((re.search('^[0-9]+$', line) is None) and (re.search('^[0-9]{2}:[0-9]{2}:[0-9]{2}', line) is None) and (re.search('^$', line) is None)):
			if (line[0]=='(') :
				line = line.lstrip('(')
				line = (line.rstrip(')+\n')).upper()
				translation = translate_and_parse(subscriptionKey, params, line) # this is the part that does the translation
				outfile.write('('+translation.rstrip()+')\n')
			else:
				# input line into translator, and remove whitespace at the end
				translation = translate_and_parse(subscriptionKey, params, line.rstrip())
				outfile.write(translation+'\n')
		else:
			outfile.write(line)

	outfile.close()
	infile.close()
	print("Finished converting %s from %s to %s." %(infile.name, fromlang, tolang))
	return


