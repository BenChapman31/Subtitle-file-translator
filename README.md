# Subtitle-file-translator
Translate a ".srt" file into a new language using the Microsoft Translator Text API.

This small Python program takes an srt file in one language and produces a new srt file in a new language, which can use a different script. Much of this code is taken directly from Microsoft tutorials, and other places on the web.

You MUST use Python3

You will need an Azure subscription key to use this, and you can sign up here:
https://docs.microsoft.com/en-us/azure/cognitive-services/translator/translator-text-how-to-signup
At the time of writing, it will let any user translate up to 2 million characters a month for free, and there's no expiration date. For licensing information for the API code, please see the relevant GitHub page.

There are many ways in which these routines and this package can be  made more sophisticated. I've only cobbled these functions together so they can produce a reasonable srt file quickly. All this assumes a common srt file format, if you find an srt file that fails to translate properly using this, please email me and I'll work on extending this to be more robust. This hasn't been extensively tested. Again, if you find a language or script for which this fails, please email me at bc661@alumni.york.ac.uk. Of course, the translations themselves are never perfect, so some of the translated srt file might be nonsense in the new language. Best to get a native speaker to do it for you...

Please feel free to email with any other suggestions!

TO DO:

1) Support for multiple APIs, e.g. Google.
2) Dictionary mapping common languages to their respective language codes.
3) Demonstrate the use of a wider range of "params".
4) GUI?
