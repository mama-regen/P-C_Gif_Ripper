####Princess & Conquest Gif Ripper
---

Decrypter adapted from <http://uuksu.fi/other/RPGMakerDecrypter>

This is meant to rip the adult animations and convert them in to GIFs _specifically_ for "Princess & Conquest."

***You must have Python3 installed for this to work.***

Click on "Run.bat" to install necessary Python libraries and run the program.
The default configuration is to export the images at their default size into the "pic_dump" folder.
The GifMaker constructor in "Program.py" takes the optional arguments "scale" and "blur" in case you want to try
and get a bigger picture out of it. That will take longer though. You can also customize where it dumps the images
and gets the encrypted archive file in there as well.
It is unlikely that I will update this at all, but it's python so it shouldn't be hard to modify. Use tkinter to
throw a GUI on or something. Go nuts.

#####Files:
>**Program** and **GifMaker** are written pretty much just for this, so they don't have a lot of utility otherwise.
>They don't really have any funtionality worth making anything out of them.

>**DataTypes** contains an *int_32* class to extend the base int class because I was tired of fucking around with bit
>lengths to make sure the keys for decrypting were correct. It also has a basic *enum* class I ripped off of
>Stack Overflow. I guess there's an official enum library for Python now but like... why bother?

>**ByteReader** is meant to mimick the C# byte reader. It has an enum for seek origin. It uses int_32 as well so
>you'll either need to take the DataTypes library with it or update it to not use those things.

>**Decrypt** is a python version of [uuksu's RPGDecrypter](http://uuksu.fi/other/RPGMakerDecrypter), but slimmed down 
>to only the stuff I specifically needed for this.

I wouldn't necessarily recommend using any of these libraries since they're garbage but do whatever I'm not your
dad. I just wanted to click a button to get porn and I'm kind enough to share that with you. You're welcome.