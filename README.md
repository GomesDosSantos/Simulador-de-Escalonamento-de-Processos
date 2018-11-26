# SImulador-de-Escalonamento-de-Processos

<img src="https://img.shields.io/pypi/pyversions/Django.svg" />

<p>Simula a execução de processos, utilizando-se de algoritmos de escanlonamento, feito pelo Sistema Operacional.</p>
<p>Os escalonadores presentes na simulação são: <a href="#first-come-first-service"><i>First-Come First-Service</i></a> (FCFS),
<a href="#shortest-job-first"><i>Shortest Job First</i></a> (SJF),
<a href="#shortest-remaining-time-first"><i>Shortest-Remaining-Time First</i></a> (SRTF), <a href="#roundrobin"><i>RoundRobin</i></a>
e uma fila <a href="#multinível"><i>multinível</i></a>.</p>

<h2>Execução</h2>
Por linha de comando:</br>
<code>$ python "Simulador de Escalonadores.py"</code>

<h2>Algoritmos</h2>
<h3>First-Come First-Service</h3>
<p>Funciona utilizando-se do princípio de que o primeiro que entra é o primeiro que sai.</p>
<h3>Shortest Job First</h3>
<p>Dentre todos os processos na fila de processos, os que possuem o menor tempo de burst serão executados em primeiro lugar.</p>
<h3>Shortest-Remaining-Time First</h3>
<p>Dentro todos os processos na fila de processos, os que possuem o menor tempo restante de burst (tempo até finalizar a execução) serão executados em primeiro lugar.</p>
<h3>RoundRobin</h3>
<p>Adiciona a premissa de compartilhamento de tempo, onde para um usuário pode dar a sensação de executando tudo ao mesmo tempo de forma paralela.</p>
<h3>Multinível</h3>
<p>Muito mais adotada pelos Sistemas Operacionais da atualidade, utiliza-se de vários algoritmos para executar os processos.
 Primeiramente com RoundRobin e após determinado tempo, dado processo ainda não terminou de executar, ele é mandado para outra fila
 com possivelmente outro algoritmo de execução como o First-Come First-Service. Em um ambiente real os processos podem trocar de
 filas durante a execução como por exemplo, minimizar uma janela.</p>

