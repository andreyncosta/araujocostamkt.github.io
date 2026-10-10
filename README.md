# Fukurō

Site institucional da Fukurō — consultoria em eficiência digital (automação, KPIs e mapeamento de processos).

🔗 **Live:** [fukuroconsultoria.com.br](https://fukuroconsultoria.com.br)

## Sobre

Landing page de página única (one-pager) apresentando os serviços da consultoria: diagnóstico de maturidade digital, automação de processos, inteligência de dados e workshops/mentorias. Construída em HTML/CSS puro, sem frameworks ou build step.

## Estrutura

```
araujocostamkt.github.io/
├── index.html              # Landing page da Fukurō (site principal)
├── atividade.html          # Página avulsa de apoio didático (download de PDFs de matemática)
├── lista_media_mediana.pdf
├── provao_matematica.pdf
└── CNAME                   # Domínio customizado: fukuroconsultoria.com.br
```

> Nota: `atividade.html` e os PDFs associados não fazem parte do site da Fukurō — são materiais de apoio hospedados no mesmo domínio do GitHub Pages.

## Deploy

Hospedado via **GitHub Pages**, com domínio customizado configurado em `CNAME`. Qualquer push para a branch padrão é publicado automaticamente — não há passo de build.

## Editar localmente

Como é HTML estático, basta abrir `index.html` diretamente no navegador ou servir a pasta com qualquer servidor estático, por exemplo:

```bash
python3 -m http.server 8000
```

## Observação sobre o formulário de contato

O formulário na seção `#contato` (`index.html`) usa `action="#"`, ou seja, ainda não envia os dados para nenhum backend ou serviço de e-mail. Para capturar leads é necessário integrá-lo a um serviço como Formspree, um endpoint próprio, ou `mailto:`.

## An?lise eleitoral p?blica

A edi??o independente est? em `/analise-candidaturas/`: visualiza??o editorial escura com evolu??o por espectro, cruzamentos municipais e pain?is individuais. Inclui 48.544 candidaturas com vota??o pr?pria, 45.107 com informa??o territorial e dez indicadores IBGE para 5.570 munic?pios. A captura e as limita??es est?o documentadas na p?gina. N?o ? apura??o em tempo real.

Somente dados derivados p?blicos s?o publicados. Os bancos SQLite, identificadores pessoais privados e revis?es privadas n?o integram este reposit?rio. O projeto original de candidaturas permanece separado.

Para gerar outra captura, execute `python tools/export_analysis.py --database CAMINHO_DO_BANCO_PRIVADO --output PASTA_NOVA`. O exportador abre o banco somente para leitura e recusa sobrescrever arquivos. Revise os resultados antes de substituir a pasta p?blica `analise-candidaturas/data`. Sirva o site por HTTP para usar os filtros.

A edi??o tamb?m foi publicada na Hostinger em https://fukuroconsultoria.com.br/analise-candidaturas/, pois o DNS do dom?nio aponta para essa hospedagem. O diret?rio ? independente do aplicativo existente na raiz.
