#SILLY MARKDOWN PARSER
import sys
import re

inf = sys.argv[1]
outf = sys.argv[1][:-2] + 'html'  

print("IN FILE: " + inf + " OUTFILE: " + outf)

#REGEX
header_p = r'#+' 
strong_1 = r'\*\*(.+)\*\*'
strong_2 = r'\_\_(.+)\_\_'
italics_1 = r'\*(.*)\*'
italics_2 = r"\_(.*)\_"
hyperlink = r'\[(.+)\]\((https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+)\)'
blockquote = r'>(.+)'
hbreak = r'-{3,}|\*{3,}|_{3,}'
imager = r'\!\[(.+)\]\s*\((.+)\"(.+)\"\)'
#\!\[(.+)\]\s*\((https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+)\s+\"(.+)\"\)
inlinecode = r'\`(.+)\`'
multilinecode = r'```(.+)```'
unorderedl = r'^(\+|\*|\-)(.+)'
orderedl = r'^([0-9]\.)+(.+)'
lmod = r'<li>(.+)</li>'

'''def add_p_tag(text):
	lines = text.split('')
	res = []
	nlines = len(lines)'''


def parse_header(text):
	lines = text.split("\n")
	res = []
	for line in lines:
		tokens = line.split(" ")
		if re.match(header_p, tokens[0]) != None:
			i = len(re.match(header_p, tokens[0]).group())
			tokens[-1] = tokens[-1].strip()
			myline = '<h'+str(i)+'>'+ " ".join(tokens[1:])+'</h'+str(i)+'>\n'
			res.append(myline)
		else:
			res.append(line)

	print("\n".join(res))
	return " <br> ".join(res)

def parse_unordered(text):
	lines = text.split('\n')
	res = []
	nlines = len(lines)
	for i in range(nlines):
		if(re.match(unorderedl, lines[i]) != None):
			if(i == 0):
				res.append("<ul>")
			elif(re.match(lmod, lines[i-1]) == None):
				res.append("<ul>")
			lines[i] = re.sub(unorderedl, r'<li> \2 </li>' , lines[i])
			res.append(lines[i])
			if(i == nlines-1):
				res.append("</ul>")
			elif(re.match(unorderedl, lines[i+1]) == None):
				res.append("</ul>")
		else:
			res.append(lines[i])
	return "\n".join(res)

def parse_ordered(text):
	lines = text.split('\n')
	res = []
	nlines = len(lines)
	for i in range(nlines):
		if(re.match(orderedl, lines[i]) != None):
			if(i == 0):
				res.append("<ol>")
			elif(re.match(lmod, lines[i-1]) == None):
				res.append("<ol>")
			lines[i] = re.sub(orderedl, r'<li> \2 </li>' , lines[i])
			res.append(lines[i])
			if(i == nlines-1):
				res.append("</ol>")
			elif(re.match(orderedl, lines[i+1]) == None):
				res.append("</ol>")
		else:
			res.append(lines[i])
	return "\n".join(res)

def sub_bold(text):
	temp1 = re.sub(strong_1, r'<strong> \1 </strong>' , text,re.DOTALL)
	return re.sub(strong_2, r'<strong> \1 </strong>' , temp1,re.DOTALL)
	
def sub_italics(text):
	temp1 = re.sub(italics_1, r'<em> \1 </em>' , text,re.DOTALL)
	return re.sub(italics_2, r'<em> \1 </em>' , temp1,re.DOTALL)

def sub_hyperlink(text):
	return re.sub(hyperlink, r"<a href='\2'> \1 </a>" , text,re.DOTALL)

def sub_block(text):
	return re.sub(blockquote, r'<blockquote> \1 </blockquote>', text, re.DOTALL)

def sub_hbreak(text):
	return re.sub(hbreak, r'<hr>', text)

def sub_image(text):
	return re.sub(imager, r"<img src='\2' alt='\1' title='\3'>", text, re.DOTALL)

def sub_inlinecode(text):
	return re.sub(inlinecode, r"<code> \1 <code>", text)

def sub_multilinecode(text):
	return re.sub(multilinecode, r"<code> \1 <code>", text, re.DOTALL)

infile = open(inf, 'r')
te = infile.read()

#PARSE ALL 
te = sub_block(te)
te = parse_unordered(te)
te = parse_ordered(te)
te = parse_header(te)
te = sub_bold(te)
te = sub_italics(te)
te = sub_hyperlink(te)
te = sub_hbreak(te)
te = sub_multilinecode(te)
te = sub_inlinecode(te)

print("After PARSE: ")
print(te)

outfile = open(outf, 'w')
te = "<html> <head>\n <title>" + outf + "</title>\n</head>\n<body>" + te + "</body>"
outfile.write(te)
infile.close()
outfile.close()