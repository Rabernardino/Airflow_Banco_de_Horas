
<h1>Extração e Envio de Relatórios de Banco de Horas</h1>

🎯 Objetivos do Projeto

O objetivo do projeto foi automatizar todo o processo de geração e envio dos relatórios de banco de horas, eliminando a necessidade de intervenção manual. A efetividade da solução é mensurável, já que reduziu o tempo gasto de aproximadamente 3 horas semanais de atividades dos colaboradores para menos de 5 minutos de execução automatizada. A sua relevância se evidencia ao liberar os colaboradores para atividades mais estratégicas, além de reduzir riscos operacionais associados ao tratamento manual dos dados.

🚀 Fluxo de Execução

O fluxo automatizado orquestrado pelo Airflow é composto pelas seguintes etapas:
<ol>
    <li>Extração de Dados: Conexão com o banco de dados do ERP para obter as informações atualizadas.</li>
    <li>Tratamento dos Dados: Processamento do DataFrame para separar os registros por gerente.</li>
    <li>Geração de Arquivos XLSX: Criação de um arquivo separado para cada gerente.</li>
    <li>Envio de E-mails: Disparo de e-mails automáticos para cada gerente, com seu respectivo arquivo anexado.</li>
</ol>

⚙️ Tecnologias Utilizadas
  <ul>
    <li>Python</li>
    <li>Apache Airflow</li>
    <li>Pandas</li>
    <li>PostgreSQL</li>
    <li>SMTP</li>
    <li>Docker</li>
  </ul>

📈 Benefícios Obtidos
<ul>
    <li>Economia de Tempo: Redução de aproximadamente 144 horas por ano em atividades operacionais.</li>
    <li>Redução de Erros: Eliminação de falhas humanas no tratamento e no envio dos arquivos.</li>
    <li>Padronização: Geração consistente de relatórios, com formato e conteúdo uniformizados.</li>
    <li>Escalabilidade: Fácil adaptação para novos gerentes ou alterações de layout dos relatórios.</li>
    <li>Documentação e Manutenção: Código versionado e documentado, facilitando futuras atualizações.</li>
</ul>



