from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import count, col
import pyspark.sql.functions as f

# set conf
conf = (
SparkConf()
    .set("spark.hadoop.fs.s3a.fast.upload", True)
    .set("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    .set('spark.hadoop.fs.s3a.aws.credentials.provider', 'com.amazonaws.auth.EnvironmentVariableCredentialsProvider')
    .set('spark.jars.packages', 'org.apache.hadoop:hadoop-aws:2.7.3')
)

# apply config
sc = SparkContext(conf=conf).getOrCreate()

def renomear_colunas(df_pnad):
    df_pnad = (
        df_pnad
        .withColumnRenamed('Ano'               , 'NU_ANO_REFERENCIA')
        .withColumnRenamed('UF'                , 'CO_UF')
        .withColumnRenamed('CAPITAL'           , 'CO_CAPITAL')
        .withColumnRenamed('RM_RIDE'           , 'CO_REGIAO_METROPOLITANA')
        .withColumnRenamed('V1012'             , 'NU_SEMANA_MES')
        .withColumnRenamed('V1013'             , 'NU_MES')   
        .withColumnRenamed('V1022'             , 'CO_SITUACAO_DOMICILIO')
        .withColumnRenamed('V1023'             , 'CO_TIPO_AREA')
        .withColumnRenamed('A001A'             , 'CO_CONDICAO_DOMICILIO')
        .withColumnRenamed('A001B1'            , 'NU_DIA_NASCIMENTO')
        .withColumnRenamed('A001B2'            , 'NU_MES_NASCIMENTO')
        .withColumnRenamed('A001B3'            , 'NU_ANO_NASCIMENTO')
        .withColumnRenamed('A002'              , 'NU_IDADE_MORADOR')
        .withColumnRenamed('A003'              , 'CO_SEXO')  
        .withColumnRenamed('A004'              , 'CO_COR') 
        .withColumnRenamed('A005'              , 'CO_ESCOLARIDADE') 
        .withColumnRenamed('A006'              , 'CO_FREQUENTA_ESCOLA') 
        .withColumnRenamed('A006A'             , 'CO_TIPO_ESCOLA') 
        .withColumnRenamed('A006B'             , 'CO_AULA_PRESENCIAL') 
        .withColumnRenamed('A007'              , 'CO_TEVE_ATIVIDADE_CASA')  
        .withColumnRenamed('A007A'             , 'CO_MOTIVO_NAO_REALIZOU_ATIVIDADE') 
        .withColumnRenamed('A008'              , 'CO_DIAS_DEDICADO_ATIVIDADE') 
        .withColumnRenamed('A009'              , 'CO_TEMPO_DEDICADO_ATIVIDADE')
        .withColumnRenamed('C011A12'           , 'NU_REMUNERACAO_TOTAL_EM_DINHEIRO') 
        .withColumnRenamed('C011A22'           , 'NU_REMUNERACAO_TOTAL_EM_PRODUTOS')   
    )
    return df_pnad

def ajuste_tipo_de_dado(df_pnad):
    df_pnad = (
        df_pnad
        .withColumn("NU_ANO_REFERENCIA"                           , f.col('NU_ANO_REFERENCIA').cast('int'))
        .withColumn("CO_UF"                                       , f.col('CO_UF').cast('int'))
        .withColumn("CO_CAPITAL"                                  , f.col('CO_CAPITAL').cast('int'))
        .withColumn("CO_REGIAO_METROPOLITANA"                     , f.col('CO_REGIAO_METROPOLITANA').cast('int'))
        .withColumn("NU_SEMANA_MES"                               , f.col('NU_SEMANA_MES').cast('int'))
        .withColumn("NU_MES"                                      , f.col('NU_MES').cast('int'))
        .withColumn("CO_SITUACAO_DOMICILIO"                       , f.col('CO_SITUACAO_DOMICILIO').cast('int'))
        .withColumn("CO_TIPO_AREA"                                , f.col('CO_TIPO_AREA').cast('int'))
        .withColumn("CO_CONDICAO_DOMICILIO"                       , f.col('CO_CONDICAO_DOMICILIO').cast('int'))
        .withColumn("NU_DIA_NASCIMENTO"                           , f.col('NU_DIA_NASCIMENTO').cast('int'))
        .withColumn("NU_MES_NASCIMENTO"                           , f.col('NU_MES_NASCIMENTO').cast('int'))
        .withColumn("NU_ANO_NASCIMENTO"                           , f.col('NU_ANO_NASCIMENTO').cast('int'))
        .withColumn("NU_IDADE_MORADOR"                            , f.col('NU_IDADE_MORADOR').cast('int'))
        .withColumn("CO_SEXO"                                     , f.col('CO_SEXO').cast('int'))
        .withColumn("CO_COR"                                      , f.col('CO_COR').cast('int'))
        .withColumn("CO_ESCOLARIDADE"                             , f.col('CO_ESCOLARIDADE').cast('int')) 
        .withColumn("CO_FREQUENTA_ESCOLA"                         , f.col('CO_FREQUENTA_ESCOLA').cast('int'))
        .withColumn("CO_TIPO_ESCOLA"                              , f.col('CO_TIPO_ESCOLA').cast('int'))
        .withColumn("CO_AULA_PRESENCIAL"                          , f.col('CO_AULA_PRESENCIAL').cast('int'))
        .withColumn("CO_TEVE_ATIVIDADE_CASA"                      , f.col('CO_TEVE_ATIVIDADE_CASA').cast('int'))
        .withColumn("CO_MOTIVO_NAO_REALIZOU_ATIVIDADE"            , f.col('CO_MOTIVO_NAO_REALIZOU_ATIVIDADE').cast('int'))
        .withColumn("CO_DIAS_DEDICADO_ATIVIDADE"                  , f.col('CO_DIAS_DEDICADO_ATIVIDADE').cast('int'))
        .withColumn("CO_TEMPO_DEDICADO_ATIVIDADE"                 , f.col('CO_TEMPO_DEDICADO_ATIVIDADE').cast('int'))
        .withColumn("NU_REMUNERACAO_TOTAL_EM_DINHEIRO"            , f.col('NU_REMUNERACAO_TOTAL_EM_DINHEIRO').cast('decimal'))
        .withColumn("NU_REMUNERACAO_TOTAL_EM_PRODUTOS"            , f.col('NU_REMUNERACAO_TOTAL_EM_PRODUTOS').cast('decimal'))
    )
    return df_pnad

def mapeamento_uf(df_pnad):
    df_pnad = (
        df_pnad
        .withColumn("DESC_UF",  
        f.when(f.col("CO_UF") == 11, 'Rond??nia')
        .when(f.col("CO_UF") == 12, 'Acre') 
        .when(f.col("CO_UF") == 13, 'Amazonas')
        .when(f.col("CO_UF") == 14, 'Roraima')
        .when(f.col("CO_UF") == 15, 'Par??')
        .when(f.col("CO_UF") == 16, 'Amap??')
        .when(f.col("CO_UF") == 17, 'Tocantins')
        .when(f.col("CO_UF") == 21, 'Maranh??o')
        .when(f.col("CO_UF") == 22, 'Piau??')
        .when(f.col("CO_UF") == 23, 'Cear??')
        .when(f.col("CO_UF") == 24, 'Rio Grande do Norte')
        .when(f.col("CO_UF") == 25, 'Para??ba')
        .when(f.col("CO_UF") == 26, 'Pernambuco')
        .when(f.col("CO_UF") == 27, 'Alagoas')
        .when(f.col("CO_UF") == 28, 'Sergipe')
        .when(f.col("CO_UF") == 29, 'Bahia')
        .when(f.col("CO_UF") == 31, 'Minas Gerais')
        .when(f.col("CO_UF") == 32, 'Esp??rito Santo')
        .when(f.col("CO_UF") == 33, 'Rio de Janeiro')
        .when(f.col("CO_UF") == 35, 'S??o Paulo')
        .when(f.col("CO_UF") == 41, 'Paran??')
        .when(f.col("CO_UF") == 42, 'Santa Catarina')
        .when(f.col("CO_UF") == 43, 'Rio Grande do Sul')
        .when(f.col("CO_UF") == 50, 'Mato Grosso do Sul')
        .when(f.col("CO_UF") == 51, 'Mato Grosso')
        .when(f.col("CO_UF") == 52, 'Goi??s')
        .when(f.col("CO_UF") == 53, 'Distrito Federal')
    ))
    return df_pnad

def mapeamento_regiao_pais(df_pnad):
    df_pnad = (
        df_pnad
        .withColumn("DESC_REGIAO_PAIS",  
        f.when((f.col("CO_UF") >= 11) &  (f.col("CO_UF") <= 17), 'NORTE')              
         .when((f.col("CO_UF") >= 21) &  (f.col("CO_UF") <= 29), 'NORDESTE')
         .when((f.col("CO_UF") >= 31) &  (f.col("CO_UF") <= 35), 'SUDESTE')
         .when((f.col("CO_UF") >= 41) &  (f.col("CO_UF") <= 43), 'SUL')
         .when((f.col("CO_UF") >= 50) &  (f.col("CO_UF") <= 53), 'CENTRO-OESTE')
    ))
    return df_pnad

def mapeamento_capital(df_pnad):
    df_pnad = (
        df_pnad
        .withColumn("DESC_CAPITAL",  
        f.when(f.col("CO_CAPITAL") == 11, 'Munic??pio de Porto Velho (RO)')
        .when(f.col("CO_CAPITAL") == 12, 'Munic??pio de Rio Branco (AC)') 
        .when(f.col("CO_CAPITAL") == 13, 'Munic??pio de Manaus (AM)')    
        .when(f.col("CO_CAPITAL") == 14, 'Munic??pio de Boa Vista (RR)') 
        .when(f.col("CO_CAPITAL") == 15, 'Munic??pio de Bel??m (PA)') 
        .when(f.col("CO_CAPITAL") == 16, 'Munic??pio de Macap?? (AP)') 
        .when(f.col("CO_CAPITAL") == 17, 'Munic??pio de Palmas (TO)')         
        .when(f.col("CO_CAPITAL") == 21, 'Munic??pio de S??o Lu??s (MA)')    
        .when(f.col("CO_CAPITAL") == 22, 'Munic??pio de Teresina (PI)') 
        .when(f.col("CO_CAPITAL") == 23, 'Munic??pio de Fortaleza (CE)') 
        .when(f.col("CO_CAPITAL") == 24, 'Munic??pio de Natal (RN)')  
        .when(f.col("CO_CAPITAL") == 25, 'Munic??pio de Jo??o Pessoa (PB)')
        .when(f.col("CO_CAPITAL") == 26, 'Munic??pio de Recife (PE)')  
        .when(f.col("CO_CAPITAL") == 27, 'Munic??pio de Macei?? (AL)')
        .when(f.col("CO_CAPITAL") == 28, 'Munic??pio de Aracaju (SE)')  
        .when(f.col("CO_CAPITAL") == 29, 'Munic??pio de Salvador (BA)')
        .when(f.col("CO_CAPITAL") == 31, 'Munic??pio de Belo Horizonte (MG)')  
        .when(f.col("CO_CAPITAL") == 32, 'Munic??pio de Vit??ria (ES)')
        .when(f.col("CO_CAPITAL") == 33, 'Munic??pio de Rio de Janeiro (RJ)')  
        .when(f.col("CO_CAPITAL") == 35, 'Munic??pio de S??o Paulo (SP)')
        .when(f.col("CO_CAPITAL") == 41, 'Munic??pio de Curitiba (PR)')  
        .when(f.col("CO_CAPITAL") == 42, 'Munic??pio de Florian??polis (SC)')
        .when(f.col("CO_CAPITAL") == 43, 'Munic??pio de Porto Alegre (RS)')
        .when(f.col("CO_CAPITAL") == 50, 'Munic??pio de Campo Grande (MS)')
        .when(f.col("CO_CAPITAL") == 51, 'Munic??pio de Cuiab?? (MT)')                
        .when(f.col("CO_CAPITAL") == 52, 'Munic??pio de Goi??nia (GO)')
        .when(f.col("CO_CAPITAL") == 53, 'Munic??pio de Bras??lia (DF)')   
    ))
    return df_pnad

def mapeamento_regiao_metropolitana(df_pnad):
    df_pnad = (
        df_pnad
        .withColumn("DESC_REGIAO_METROPOLITANA",  
        f.when(f.col("CO_REGIAO_METROPOLITANA") == 13, 'Regi??o Metropolitana de Manaus (AM)')
        .when(f.col("CO_REGIAO_METROPOLITANA") == 15, 'Regi??o Metropolitana de Bel??m (PA)') 
        .when(f.col("CO_REGIAO_METROPOLITANA") == 16, 'Regi??o Metropolitana de Macap?? (AP)') 
        .when(f.col("CO_REGIAO_METROPOLITANA") == 21, 'Regi??o Metropolitana de Grande S??o Lu??s (MA)') 
        .when(f.col("CO_REGIAO_METROPOLITANA") == 22, 'Regi??o Administrativa Integrada de Desenvolvimento da Grande Teresina (PI)')     
        .when(f.col("CO_REGIAO_METROPOLITANA") == 23, 'Regi??o Metropolitana de Fortaleza (CE)') 
        .when(f.col("CO_REGIAO_METROPOLITANA") == 24, 'Regi??o Metropolitana de Natal (RN)') 
        .when(f.col("CO_REGIAO_METROPOLITANA") == 25, 'Regi??o Metropolitana de Jo??o Pessoa (PB)') 
        .when(f.col("CO_REGIAO_METROPOLITANA") == 26, 'Regi??o Metropolitana de Recife (PE)')  
        .when(f.col("CO_REGIAO_METROPOLITANA") == 27, 'Regi??o Metropolitana de Macei?? (AL)') 
        .when(f.col("CO_REGIAO_METROPOLITANA") == 28, 'Regi??o Metropolitana de Aracaju (SE)') 
        .when(f.col("CO_REGIAO_METROPOLITANA") == 29, 'Regi??o Metropolitana de Salvador (BA)') 
        .when(f.col("CO_REGIAO_METROPOLITANA") == 31, 'Regi??o Metropolitana de Belo Horizonte (MG)')     
        .when(f.col("CO_REGIAO_METROPOLITANA") == 32, 'Regi??o Metropolitana de Grande Vit??ria (ES)') 
        .when(f.col("CO_REGIAO_METROPOLITANA") == 33, 'Regi??o Metropolitana de Rio de Janeiro (RJ)') 
        .when(f.col("CO_REGIAO_METROPOLITANA") == 35, 'Regi??o Metropolitana de S??o Paulo (SP)') 
        .when(f.col("CO_REGIAO_METROPOLITANA") == 41, 'Regi??o Metropolitana de Curitiba (PR)')  
        .when(f.col("CO_REGIAO_METROPOLITANA") == 42, 'Regi??o Metropolitana de Florian??polis (SC)') 
        .when(f.col("CO_REGIAO_METROPOLITANA") == 43, 'Regi??o Metropolitana de Porto Alegre (RS)')  
        .when(f.col("CO_REGIAO_METROPOLITANA") == 51, 'Regi??o Metropolitana de Vale do Rio Cuiab?? (MT)') 
        .when(f.col("CO_REGIAO_METROPOLITANA") == 52, 'Regi??o Metropolitana de Goi??nia (GO)')                 
    ))
    return df_pnad

def mapeamento_situacao_domicilio(df_pnad):
    df_pnad = (
        df_pnad
        .withColumn("DESC_SITUACAO_DOMICILIO",  
        f.when(f.col("CO_SITUACAO_DOMICILIO") == 1, 'Urbana')
        .when(f.col("CO_SITUACAO_DOMICILIO") == 2, 'Rural') 
    ))
    return df_pnad

def mapeamento_tipo_area(df_pnad):
    df_pnad = (
        df_pnad
        .withColumn("DESC_TIPO_AREA",  
        f.when(f.col("CO_TIPO_AREA") == 1, 'Capital')
        .when(f.col("CO_TIPO_AREA") == 2, 'Resto da RM (Regi??o Metropolitana, excluindo a capital)') 
        .when(f.col("CO_TIPO_AREA") == 3, 'Resto da RIDE (Regi??o Integrada de Desenvolvimento Econ??mico, excluindo a capital) ')
        .when(f.col("CO_TIPO_AREA") == 4, 'Resto da UF  (Unidade da Federa????o, excluindo a regi??o metropolitana e a RIDE)')
    ))
    return df_pnad

def mapeamento_condicao_domicilio(df_pnad):
    df_pnad = (
        df_pnad
        .withColumn("DESC_CONDICAO_DOMICILIO",  
        f.when(f.col("CO_CONDICAO_DOMICILIO") == 1, 'Pessoa respons??vel pelo domic??lio')
        .when(f.col("CO_CONDICAO_DOMICILIO") == 2, 'C??njuge ou companheiro(a) de sexo diferente') 
        .when(f.col("CO_CONDICAO_DOMICILIO") == 3, 'C??njuge ou companheiro(a) do mesmo sexo') 
        .when(f.col("CO_CONDICAO_DOMICILIO") == 4, 'Filho(a) do respons??vel e do c??njuge')  
        .when(f.col("CO_CONDICAO_DOMICILIO") == 5, 'Filho(a) somente do respons??vel') 
        .when(f.col("CO_CONDICAO_DOMICILIO") == 6, 'Enteado(a)') 
        .when(f.col("CO_CONDICAO_DOMICILIO") == 7, 'Genro ou nora')
        .when(f.col("CO_CONDICAO_DOMICILIO") == 8, 'Pai, m??e, padrasto ou madrasta') 
        .when(f.col("CO_CONDICAO_DOMICILIO") == 9, 'Sogro(a)') 
        .when(f.col("CO_CONDICAO_DOMICILIO") == 10, 'Neto(a)')
        .when(f.col("CO_CONDICAO_DOMICILIO") == 11, 'Bisneto(a)')
        .when(f.col("CO_CONDICAO_DOMICILIO") == 12, 'Irm??o ou irm??') 
        .when(f.col("CO_CONDICAO_DOMICILIO") == 13, 'Av?? ou av??') 
        .when(f.col("CO_CONDICAO_DOMICILIO") == 14, 'Outro parente')  
        .when(f.col("CO_CONDICAO_DOMICILIO") == 15, 'Agregado(a) - N??o parente que n??o compartilha despesas') 
        .when(f.col("CO_CONDICAO_DOMICILIO") == 16, 'Convivente - N??o parente que compartilha despesas') 
        .when(f.col("CO_CONDICAO_DOMICILIO") == 17, 'Pensionista')
        .when(f.col("CO_CONDICAO_DOMICILIO") == 18, 'Empregado(a) dom??stico(a)') 
        .when(f.col("CO_CONDICAO_DOMICILIO") == 19, 'Parente do(a) empregado(a) dom??stico(a)')
    ))
    return df_pnad

def mapeamento_grupo_idade(df_pnad):
    df_pnad = (
        df_pnad
        .withColumn("NU_GRUPO_IDADE",  
        f.when((f.col("NU_IDADE_MORADOR") >= 4)  & (f.col("NU_IDADE_MORADOR") <= 5), 1)
         .when((f.col("NU_IDADE_MORADOR") >= 6)  & (f.col("NU_IDADE_MORADOR") <= 10), 2) 
         .when((f.col("NU_IDADE_MORADOR") >= 11) & (f.col("NU_IDADE_MORADOR") <= 14), 3)
         .when((f.col("NU_IDADE_MORADOR") >= 15) & (f.col("NU_IDADE_MORADOR") <= 17), 4)
         .when((f.col("NU_IDADE_MORADOR") > 17), 5)
         .otherwise(0)
    ))

def mapeamento_faixa_etaria(df_pnad):
    df_pnad = (
        df_pnad
        .withColumn("DESC_FAIXA_ETARIA",  
        f.when(f.col("NU_GRUPO_IDADE") == 2, 'De 6 a 10 anos') 
        .when(f.col("NU_GRUPO_IDADE") == 3, 'De 11 a 14 anos') 
        .when(f.col("NU_GRUPO_IDADE") == 4, 'De 15 a 17 anos') 
        .otherwise("N??o aplic??vel") 
    ))

def mapeamento_sexo(df_pnad):
    df_pnad = (
        df_pnad
        .withColumn("DESC_SEXO",  
        f.when(f.col("CO_SEXO") == 1, 'Masculino')
        .when(f.col("CO_SEXO") == 2, 'Feminino') 
    ))
    return df_pnad

def mapeamento_cor(df_pnad):
    df_pnad = (
        df_pnad
        .withColumn("DESC_COR",  
        f.when(f.col("CO_COR") == 1, 'Branca')
        .when(f.col("CO_COR") == 2, 'Preta')
        .when(f.col("CO_COR") == 3, 'Amarela')
        .when(f.col("CO_COR") == 4, 'Parda')
        .when(f.col("CO_COR") == 5, 'Ind??gina')
        .when(f.col("CO_COR") == 9, 'Ignorado')
    ))
    return df_pnad

def mapeamento_escolaridade(df_pnad):
    df_pnad = (
        df_pnad
        .withColumn("DESC_ESCOLARIDADE",  
        f.when(f.col("CO_ESCOLARIDADE") == 1, 'Sem instru????o')
        .when(f.col("CO_ESCOLARIDADE") == 2, 'Fundamental incompleto') 
        .when(f.col("CO_ESCOLARIDADE") == 3, 'Fundamental completa')
        .when(f.col("CO_ESCOLARIDADE") == 4, 'M??dio incompleto')
        .when(f.col("CO_ESCOLARIDADE") == 5, 'M??dio completo')
        .when(f.col("CO_ESCOLARIDADE") == 6, 'Superior incompleto')
        .when(f.col("CO_ESCOLARIDADE") == 7, 'Superior completo')
        .when(f.col("CO_ESCOLARIDADE") == 8, 'P??s-gradua????o, mestrado ou doutorado')
    ))
    return df_pnad

def mapeamento_frequenta_escola(df_pnad):
    df_pnad = (
        df_pnad
        .withColumn("DESC_FREQUENTA_ESCOLA",  
        f.when(f.col("CO_FREQUENTA_ESCOLA") == 1, 'Sim')
        .when(f.col("CO_FREQUENTA_ESCOLA") == 2, 'N??o') 
        .otherwise('N??o aplic??vel')         
    ))
    return df_pnad

def mapeamento_tipo_escola(df_pnad):
    df_pnad = (
        df_pnad
        .withColumn("DESC_TIPO_ESCOLA",  
        f.when(f.col("CO_TIPO_ESCOLA") == 1, 'P??blica')
        .when(f.col("CO_TIPO_ESCOLA") == 2, 'Privada') 
        .otherwise('N??o aplic??vel')         
    ))
    return df_pnad

def mapeamento_aula_presencial(df_pnad):
    df_pnad = (
        df_pnad
        .withColumn("DESC_AULA_PRESENCIAL",  
        f.when(f.col("CO_AULA_PRESENCIAL") == 1, 'Sim, normalmente')
        .when(f.col("CO_AULA_PRESENCIAL") == 2, 'Sim, mas apenas parcialmente') 
        .when(f.col("CO_AULA_PRESENCIAL") == 3, 'N??o, e meu normalmente ?? presencial/semipresencial')
        .when(f.col("CO_AULA_PRESENCIAL") == 4, 'N??o, meu curso ?? online')
        .otherwise('N??o aplic??vel')         
    ))    

def mapeamento_teve_atividade_casa(df_pnad):
    df_pnad = (
        df_pnad
        .withColumn("DESC_TEVE_ATIVIDADE_CASA",  
        f.when(f.col("CO_TEVE_ATIVIDADE_CASA") == 1, 'Sim, e realizou pelo menos parte delas')
         .when(f.col("CO_TEVE_ATIVIDADE_CASA") == 2, 'Sim, mas n??o realizou (por qualquer motivo)') 
         .when(f.col("CO_TEVE_ATIVIDADE_CASA") == 3, 'N??o')
         .when(f.col("CO_TEVE_ATIVIDADE_CASA") == 3, 'N??o, porque estava de f??rias')
         .otherwise('N??o aplic??vel')  
    ))
    return df_pnad

def mapeamento_motivo_nao_realizou_atividade(df_pnad):
    df_pnad = (
        df_pnad
        .withColumn("DESC_MOTIVO_NAO_REALIZOU_ATIVIDADE",  
        f.when(f.col("CO_MOTIVO_NAO_REALIZOU_ATIVIDADE") == 1, 'N??o tinha computador / tablet / celular dispon??vel')
        .when(f.col("CO_MOTIVO_NAO_REALIZOU_ATIVIDADE") == 2, 'N??o tinha acesso ?? internet ou a qualidade dela era insuficiente') 
        .when(f.col("CO_MOTIVO_NAO_REALIZOU_ATIVIDADE") == 3, 'Por problemas de sa??de da pr??pria pessoa')
        .when(f.col("CO_MOTIVO_NAO_REALIZOU_ATIVIDADE") == 4, 'Tinha que cuidar dos afazeres dom??sticos, do(s) filhos ou de outro(s) parentes')
        .when(f.col("CO_MOTIVO_NAO_REALIZOU_ATIVIDADE") == 5, 'N??o conseguiu se concentrar')
        .when(f.col("CO_MOTIVO_NAO_REALIZOU_ATIVIDADE") == 6, 'Outro motivo. Especifique.')
        .otherwise('N??o aplic??vel')  
    ))
    return df_pnad

def mapeamento_dias_dedicacao_atividade(df_pnad):
    df_pnad = (
        df_pnad
        .withColumn("DESC_DIAS_DEDICADO_ATIVIDADE",  
        f.when(f.col("CO_DIAS_DEDICADO_ATIVIDADE") == 1, '1 dia')
         .when(f.col("CO_DIAS_DEDICADO_ATIVIDADE") == 2, '2 dias')
         .when(f.col("CO_DIAS_DEDICADO_ATIVIDADE") == 3, '3 dias')
         .when(f.col("CO_DIAS_DEDICADO_ATIVIDADE") == 4, '4 dias')
         .when(f.col("CO_DIAS_DEDICADO_ATIVIDADE") == 5, '5 dias')
         .when(f.col("CO_DIAS_DEDICADO_ATIVIDADE") == 6, '6 ou 7 dias')
         .otherwise('N??o aplic??vel') 
    ))
    return df_pnad

def mapeamento_tempo_dedicado_atividade(df_pnad):
    df_pnad = (
        df_pnad
        .withColumn("DESC_TEMPO_DEDICADO_ATIVIDADE",  
        f.when(f.col("CO_TEMPO_DEDICADO_ATIVIDADE") == 1, 'Menos de 1 hora')
         .when(f.col("CO_TEMPO_DEDICADO_ATIVIDADE") == 2, 'De 1 hora a menos de 2 horas') 
         .when(f.col("CO_TEMPO_DEDICADO_ATIVIDADE") == 3, 'De 2 horas a menos de 5 horas')
         .when(f.col("CO_TEMPO_DEDICADO_ATIVIDADE") == 4, '5 horas ou mais')
         .otherwise('N??o aplic??vel') 
    ))
    return df_pnad

if __name__ == "__main__":

    # init spark session
    spark = SparkSession\
            .builder\
            .appName("PNAD CONVID19 Job")\
            .getOrCreate()

    spark.sparkContext.setLogLevel("WARN")

    df_pnad = (
        spark
        .read
        .format("parquet")
        .load('s3a://igti-datalake-astheobaldo/datalake/landing-zone/')
    )

    print("*************************************************************************")
    print("** Tratamento - nomes de colunas, tipos de dados e mapeamento de dados **")
    print("*************************************************************************")

    df_pnad = renomear_colunas(df_pnad)
    df_pnad = ajuste_tipo_de_dado(df_pnad)
    df_pnad = mapeamento_uf(df_pnad)
    df_pnad = mapeamento_regiao_pais(df_pnad)
    df_pnad = mapeamento_capital(df_pnad)
    df_pnad = mapeamento_regiao_metropolitana(df_pnad)
    df_pnad = mapeamento_situacao_domicilio(df_pnad)
    df_pnad = mapeamento_tipo_area(df_pnad)
    df_pnad = mapeamento_condicao_domicilio(df_pnad)
    df_pnad = mapeamento_grupo_idade(df_pnad)
    df_pnad = mapeamento_faixa_etaria(df_pnad)
    df_pnad = mapeamento_sexo(df_pnad)
    df_pnad = mapeamento_cor(df_pnad)
    df_pnad = mapeamento_escolaridade(df_pnad)
    df_pnad = mapeamento_frequenta_escola(df_pnad)
    df_pnad = mapeamento_tipo_escola(df_pnad)
    df_pnad = mapeamento_aula_presencial(df_pnad)
    df_pnad = mapeamento_teve_atividade_casa(df_pnad)
    df_pnad = mapeamento_motivo_nao_realizou_atividade(df_pnad)
    df_pnad = mapeamento_dias_dedicacao_atividade(df_pnad)
    df_pnad = mapeamento_tempo_dedicado_atividade(df_pnad)

    (
        df_pnad
        .write
        .mode("overwrite")
        .format("parquet")
        .save('s3a://igti-datalake-astheobaldo/datalake/processing-zone/')
    )

    print("**************************************")
    print("** Tratamento realizao com sucesso! **")
    print("**************************************")

    spark.stop()
    