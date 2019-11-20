import heapq
import os

# Cada nó deve ter o char correspondente e a dic_frequência que ocorre. Também deve possuir um ponteiro para um filho esquerdo e direito.
#Inicializar nó esq e dir com null
class No:
	def __init__(self, char, dic_freq):
		self.char = char
		self.dic_freq = dic_freq
		self.esq = None
		self.dir = None

	# defining comparators less_than and equals
	def __lt__(self, other):
		return self.dic_freq < other.dic_freq

	def __eq__(self, other):
		if(other == None):
			return False
		if(not isinstance(other, No)):
			return False
		return self.dic_freq == other.dic_freq


class CodificacaoHuffman:
	def __init__(self):
		self.arvore = []
		self.codigo = {}
		self.mapa_descompressao = {}

	# Cria o dicionario da partir do texto
	def criaDicionario(self, texto):
		dicionario = {}
		for character in texto:
			if character in dicionario:
				dicionario[character] += 1
			else:
				dicionario[character] = 0
		return dicionario

	def cria_no(self, dic_freq):
		for valor in dic_freq:
			no = No(valor, dic_freq[valor])
			heapq.heappush(self.arvore, no)
			

	def junta_nos(self):
		while(len(self.arvore) > 1):
			no1 = heapq.heappop(self.arvore)
			no2 = heapq.heappop(self.arvore)

			no_pai = No(None, no1.dic_freq + no2.dic_freq)
			no_pai.esq = no1
			no_pai.dir = no2

			heapq.heappush(self.arvore, no_pai)


	def cria_caminho(self, no, caminho_bin_atual):
		if(no == None):
			return

		if(no.char != None):
			self.codigo[no.char] = caminho_bin_atual
			self.mapa_descompressao[caminho_bin_atual] = no.char
			return

		self.cria_caminho(no.esq, caminho_bin_atual + "0")
		self.cria_caminho(no.dir, caminho_bin_atual + "1")


	def cria_codigo(self):
		no = heapq.heappop(self.arvore)
		caminho_bin_atual = ""
		self.cria_caminho(no, caminho_bin_atual)


	def codifica_texto(self, text):
		texto_codificado = ""
		for character in text:
			texto_codificado += self.codigo[character]
		return texto_codificado


	def completa_texto_codificado(self, texto_codificado):
		texto_extra = 8 - len(texto_codificado) % 8
		for i in range(texto_extra):
			texto_codificado += "0"

		padded_info = "{0:08b}".format(texto_extra)
		texto_codificado = padded_info + texto_codificado
		return texto_codificado


	def cria_array_byte(self, texto_codificado):
		b = bytearray()
		for i in range(0, len(texto_codificado), 8):
			byte = texto_codificado[i:i+8]
			b.append(int(byte, 2))
		return b

	def remove_preenchimento(self, texto_codificado):
		padded_info = texto_codificado[:8]
		tam_texto = int(padded_info, 2)

		texto_codificado = texto_codificado[8:]
		texto_codificado = texto_codificado[:-tam_texto]

		return texto_codificado

	def decodifica_texto(self, texto_codificado):
		binario_atual = ""
		texto_final = ""

		for bit in texto_codificado:
			binario_atual += bit
			if(binario_atual in self.mapa_descompressao):
				character = self.mapa_descompressao[binario_atual]
				texto_final += character
				binario_atual = ""

		return texto_final


	def decompress(self, input_path):
		filename, file_extension = os.path.splitext("texto.txt")
		output_path = filename + "_decompressed" + ".txt"

		with open(input_path, 'rb') as file, open(output_path, 'w') as output:
			bit_string = ""

			byte = file.read(1)
			while(len(byte) > 0):
				byte = ord(byte)
				bits = bin(byte)[2:].rjust(8, '0')
				#print(bits)
				bit_string += bits
				byte = file.read(1)

			texto_codificado = self.remove_preenchimento(bit_string)

			decompressed_text = self.decodifica_texto(texto_codificado)
			
			output.write(decompressed_text)

		print(input_path + " foi descomprimido")
		return output_path
		
def main():
	arquivo_entrada = "texto.txt"
	self = CodificacaoHuffman()
	filename, file_extension = os.path.splitext("texto.txt")
	arquivo_saida = filename + ".bin"

	with open(arquivo_entrada, 'r+') as file, open(arquivo_saida, 'wb') as output:
		text = file.read()
		text = text.rstrip()

		dic_freq = self.criaDicionario(text)
		self.cria_no(dic_freq)
		self.junta_nos()
		self.cria_codigo()

		texto_codificado = self.codifica_texto(text)
		padded_texto_codificado = self.completa_texto_codificado(texto_codificado)

		b = self.cria_array_byte(padded_texto_codificado)
		output.write(bytes(b))

	print(arquivo_entrada + " foi comprimido")

	self.decompress(arquivo_saida)

if __name__ == '__main__':
    main()