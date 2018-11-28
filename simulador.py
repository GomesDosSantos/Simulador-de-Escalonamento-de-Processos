import random
import operator

class Processo(object):
    def __init__(self, nome,burst,tcheg,tesp,turnaround,quantum,br):
        self.nome = nome    # Nome Processo
        self.burst = burst  # Burst do Processo
        self.tcheg = tcheg  # Tempo de Chegada
        self.tesp = tesp    # Tempo de Espera
        self.turnaround = turnaround # Tempo Total
        self.quantum = quantum # Tempo de Quantum
        self.br = br        # Tempo restante de Burst
        
        
    def setNome(self, nome):
        self.nome = nome

    def setBurst(self, burst):
        self.burst = burst
    
    def setTcheg(self, tcheg):
        self.tcheg = tcheg

    def setTesp(self,tesp):
        self.tesp = tesp

    def setTurnaround(self,turnaround):
        self.turnaround = turnaround
        
    def setQuantum(self,quantum):
        self.quantum = quantum

    def setBr( self , br ):
        self.br = br

# Print Padrão de saída de uma lista de Processos
def saida( processos , titulo ):
    print( '{: ^75}'.format( titulo ) )
    print( '\n\rProcesso  |  BURST  |  TCHEG  |  T.ES  |  T.TL  | Quantum' )
    for p in processos:
        print( '{: ^10}|{: ^9}|{: ^9}|{: ^8}|{: ^8}|{: ^9}'.format( p.nome , p.burst , p.tcheg , p.tesp , p.turnaround , p.quantum ) )
    avgTESP = sum([ x.tesp for x in processos ]) / len(processos)
    avgTURNAROUND = sum([ x.turnaround for x in processos ]) / len(processos)
    avgTESP = round( avgTESP ) # Arredonda a média de tempo de espera da lista de processos
    avgTURNAROUND = round( avgTURNAROUND ) # Arredonda a média de tempo de turnaround da lista de processos
    
    print( '{: ^75}'.format( f'Média de Espera: {avgTESP} | Média Turnaround: {avgTURNAROUND}' ) )
    # Média de tempo de espera | média de turnaround
    print( '\n{: ^75}\n'.format( titulo ) )
    
# Padrão de Carregamento de Arquivo
# Retorna uma lista de processos
def carregarArquivo( nome ):
    # Entrada da pasta tem que SER fornecida pelo usuário
    import re
    import string

    o = ()
    with open( '{:s}.txt'.format( nome ) , 'r' ) as a:
        o = a.readlines()
    
    l = list()

    for linha in o:
        if linha not in string.whitespace:
            l.append( re.split( r'[\W]' , linha ) )

    aux = list()
    
    for i in range( 0, len(l) ) :
        ###                   nome     burst   tempo chegada  tempo espera   turnaround quantum
        aux.append( Processo( l[i][1] , int(l[i][2]), int(l[i][3]) , int(l[i][4]) , 0 , int(l[i][5]) , 0 ) )

    return aux
    

# Calcula o tempo de ESPERA com base no burst dos processos anteriores recursivamente
#   process-lista , nº processos
def pant( lista , n ):
    if len( lista ) <= 2 or n <= 1:
        return lista[n - 1].burst
    # Significa que estamos na primeira posição cujo Tempo Espera = 0 - para p1, mas não para o p2
    else:
        return lista[ n - 1 ].burst + pant( lista , n - 1 )

# Avalia o tempo de chegada se igual a n
# Retorna uma lista com n elementos com tcheg == n
def ptcheg( lista , n ):
    r = list()
    for i in lista:
        if i.tcheg == n: r.append( i )
    return r

###========================= ALGORITMOS =========================###
# * Todos os processos retornam uma lista de processos executados

# First Come First Service
def fcfs( lista ):
    processos = list( lista ) # Cria uma cópia da lista
    # para poder usar os mesmos processos para todos os escalonadores diferentes

    # Zera o tempo de turnaround e espera de todos os processos, para poder calcular de forma correta
    for i in range( 0 , len(processos) ):
        processos[i].tesp = 0
        processos[i].turnaround = 0

    # O primeiro processo na fila não espera nada, logo
    # p turnaround = p burst
    processos[0].turnaround = processos[0].burst

    # Simula a execução dos processos em ordem de FCFS
    for i in range( 1 , len(processos) ):
        processos[i].tesp = pant( processos , i )
        processos[i].turnaround = pant( processos , i+1 )
    
    return processos
    

# Shortest Job First
# Recebe os processos, executa a ordenação pelo menor BURST
def sjf( lista ):
    processos = list( lista )
    processos.sort(key=operator.attrgetter("burst"),reverse=False)
    # Com os processos organizados
    # É possível executá-los pelo simulador

    # Primeiro processo não espera nada
    processos[0].tesp = 0
    processos[0].turnaround = processos[0].burst
    
    for i in range( 1 , len(processos) ):
        processos[i].tesp = pant( processos , i )
        processos[i].turnaround = processos[i].tesp + processos[i].burst

    # Organiza a saída por nome, mas com os valores corretos de espera, turnaround
    processos.sort(key=operator.attrgetter("nome"),reverse=False)
    
    return processos

# Shortest-Remaining-Time-First
# Ordena a lista, escuta pela chegada de novos processos
# Ordena a lista e executa os processos ATÉ chegar novos processos
def srjf( lista ):
    # Cópia de Lista de Processos
    processos = list( lista )
    # Lista de processos a ser executados
    execucao = list()
    
    # Arruma o Tempo de Burst Restante
    for p in processos:
        p.setBr( p.burst )
        if p.tcheg == 0:
            execucao.append( p ) # Adiciona os Processos que chegaram no tempo 0
    # Ordena a lista de processos a ser executada por ordem de burst restante
    execucao.sort( key = operator.attrgetter("br") , reverse = False )

    # Cálculo de um tempo padrão que será a soma total de burst de todos or processos
    burst = pant( processos , len( processos ) )

    # Executa burst por burst aqui
    for i in range( burst ):            
        
        # A posição 0 SEMPRE SERÁ ocupada telo menor tempo restante
        execucao[0].br -= 1 # Diminui o burst do processo utilizado agora
        
        # Agora, deve somar 1 ao tempo de espera de cada processo que NÃO SEJA este
        for x in range( 1 , len(execucao) ):
            execucao[x].tesp += 1

        # Receber os processos que chegaram neste i tempo
        for p in processos:
            if p.tcheg == i and p not in execucao : # Tempo de Chegada igual a esta unidade de tempo
                execucao.append( p )

        #print( len(execucao) )
        # Organiza novamente pelo menor burst restante
        execucao.sort( key = operator.attrgetter("br") , reverse = False )

        # Se o processo não tiver mais burst pra rodar, deve-se removê-lo da lista
        # E dar a vez a outro processo
        if execucao[0].br == 0:
            execucao.remove( execucao[0] )
        
    # Tempo de TurnAround dos processo
    # O Burst + Tempo de Espera Total deles
    for p in processos:
        p.turnaround = p.burst + p.tesp
        
    return processos

# RoundRobin
# Utiliza-se o Quantum para determinar quanto tempo cada processos irá ser executado pelo CPU
# Execução circular, todos executam por x unidades de tempo
# Roda pela lista de processos e os executa 1 por 1 por x quantum
def rr( lista ):
    processos = list( lista )
    quantum = 1

    # Pega o maior Quantum disponível
    for p in processos:
        quantum = p.quantum if p.quantum > quantum else quantum
        p.setBr( p.burst ) # Burst Restante
        
    # Cópia da lista de processos
    execucao = list( processos )
    
    # Zera os tempos de todos os processos
    for p in execucao:
        p.setTesp( 0 )
        p.setTurnaround( 0 )

    r =  0 # Contador de quantum
    p = -1 # Contador de Processo em Execução

    print( '\nQuantum: ' , quantum )

    # Enquanto tiver processos para executar
    while execucao:

        # Contador de processos
        p = ( p + 1 ) % len( execucao )

        # EXECUTAR professor por X unidades de Tempo
        # Calcular Quantum restante
        # Calcular Tempo de Espera dos outros processos
        # SE Processo sem quantum, removê-lo da execução

        # Execucao 1 unidade de tempo quantum
        r = execucao[ p ].br - quantum
        # Identificador de passagem
        st = True
        
        if r >= quantum:
            # Se mesmo após aplicar o quantum, o processo ainda possui tempo de burst
            execucao[ p ].setBr( r )
        else:
            if r > 0:
                execucao[ p ].setBr( r )
            else:
                # Caso o quantum SEJA MAIOR que o tempo necessário para finalizar o processo
                st = False
                r = execucao[ p ].br
                execucao[ p ].setBr( 0 )
        
        # Aumenta o tempo de espera de todos os processos que não foram executados NESTA passagem
        for ex in execucao:
            if ex != execucao[ p ]:
                ex.tesp += quantum if st else r

        if execucao[ p ].br == 0:
            processos[ processos.index( execucao[p] ) ] = execucao[ p ]
            execucao.remove( execucao[ p ] )
            # Para evitar o problema de quanto um processo é removido e
            # o contador avança e pula um processo no meio
            # Por exemplo:
            #  p0 -> p1  - p1 acabou dentro do quantum, naturalmente, p2 seria executado agora
            # Mas a lista de processos foi alterada para: p0 - p2 - p3... então
            #  p0 -> p1 -> p3 , pois p1 havia sido removido, logo, para manter a ordem
            # Diminuímos o contador de processo atual em 1
            p -= 1
        

    # Calcula o TURNAROUND de todos os processos
    for p in processos:
        p.turnaround = p.burst + p.tesp
    
    return processos

# Executa os processos pelo primeiro quantum
# retorna tuple dos processos que não finalizaram e os que finalizaram
# tuple( fcfs , FINALIZADO )
def rr2( processos , quantum ):
    #rr( processos )

    execucao = list( processos )
    nf = list() # Não finalizados
    
    r =  0 # Contador de quantum
    p = -1 # Contador de Processo em Execução

    while execucao:
        p = ( p + 1 ) % len( execucao )

        # Execucao 1 unidade de tempo quantum
        r = execucao[ p ].br - quantum
        st = True
        
        if r >= quantum:
            execucao[ p ].setBr( r )
        else:
            if r > 0:
                execucao[ p ].setBr( r )
            else:
                st = False
                r = execucao[ p ].br
                execucao[ p ].setBr( 0 )

        for ex in execucao:
            if ex != execucao[ p ]:
                ex.tesp += quantum if st else r

        # Guarda o processo não finalizado em 1 unidade de tempo quantum
        if st:
            nf.append( execucao[ p ] )
            # E então o remove da lista
            execucao.remove( execucao[ p ] )
            p -= 1
        else:
            processos[ processos.index( execucao[p] ) ] = execucao[ p ]
            execucao.remove( execucao[ p ] )
            p -= 1

    # Calcula o TURNAROUND de todos os processos
    # Que finalizaram
    for p in processos:
        if p not in nf:
            p.turnaround = p.burst + p.tesp
            execucao.append( p ) # Armazena os processos que finalizaram na lista execução

    # Não finalizados, finalizados
    return ( nf , execucao )

def fcfs2( processos ):

    for p in processos:
        # Tempo de Espera = somatório de todos os burst restantes anteriores
        p.setTesp( sum([x.br for x in processos[:processos.index(p)]]) )
        p.setTurnaround( p.tesp + p.br )

    return processos

def multinivel( lista ):
    processos = list( lista ) # Cópia

    execucao = tuple()

    # Limpa os processos dos métodos anteriores
    for p in processos:
        p.setTesp( 0 )
        p.setTurnaround( 0 )

    quantum = 1
    # Pega o maior Quantum disponível
    for p in processos:
        quantum = p.quantum if p.quantum > quantum else quantum
        p.setBr( p.burst ) # Burst Restante

    # Executa os processos em RoundRobin primeiramente
    execucao = rr2( processos , quantum )
    f = fcfs2( execucao[0] ) # Lista de processos não finalizados são mandados para um FCFS
    
    # Substituição dos processos na lista principal
    for p in execucao[1]: # Processo finalizados por RoundRobin
        p.setBr( 0 )
        processos[ processos.index( p ) ] = p
    for p in f: # Processos finalizados por FCFS
        p.setBr( 0 )
        processos[ processos.index( p ) ] = p
        
    return processos

# Padrão de Início dos processos
def iniciar():

    lista = []

    while True:
        c = input("Burst Manual, Aleatório ou por Arquivo? (M | A | B - respectivamente)\nPara sair: S\n")
        try:
            if c == "A":
                n = int(input("Qual a quantidede de processos?"))
                #burst e tempo de chegada automático
                for i in range(n):
                    proc = Processo( 'p{:}'.format(i) , random.randint(1, 100) , random.randint(0, 15) , 0 , 0 , random.randint(1,20) , 0 )
                    lista.append(proc)
            elif c == "B":
                nome = input("Digite o nome do arquivo (sem .txt):")
                print( f'Tentativa de carregar o arquivo: {nome}.txt' )
                lista = carregarArquivo( nome ) # RETORNARÁ a lista de Objetos
            elif c == "M":
                n = int(input("Qual a quantidede de processos?"))
                #burst e tempo de chegada manual
                for i in range(n):
                    b = int(input("P" + str(i) +" Burst:"))
                    t = int(input("P" + str(i) +" Tempo de Chegada:"))
                    q = int(input("P" + str(i) + " Quantum: " ) )
                    proc = Processo( 'p{:}'.format(i) , b , t , 0 , 0 , q , 0 )
                    lista.append(proc)
            #else:
                #exit( 0 )
        except:
            print( 'Entrada inválida' )
            #exit( 0 )
            # Executa e mostra o resultado de todos os simuladores
        saida( fcfs(lista) , 'FCFS' )
        saida( sjf(lista) , 'SJF' )
        saida( srjf(lista) , 'SRJF' )
        saida( rr(lista) , 'Round Robin' )
        saida( multinivel(lista) , 'Multinível' )


## Main
if __name__ == '__main__':

    # Iniciar e carregar qualquer coisa que seja necessária
    iniciar()
