import pika
import json
import time

def processar_log(ch, method, properties, body):
    """
    Função de Callback: O que o worker faz quando recebe uma mensagem.
    """
    mensagem = json.loads(body)
    
    print(f"\n[📥] Nova mensagem recebida da fila!")
    print(f"     Serviço: {mensagem.get('service')}")
    print(f"     Log: {mensagem.get('message')}")
    
    # Simulando um processamento pesado (ex: gravando num Data Lake ou ElasticSearch)
    time.sleep(2) 
    
    print("[✅] Log processado com sucesso.")
    
    # Avisa ao RabbitMQ que a mensagem foi processada e pode ser apagada da fila
    ch.basic_ack(delivery_tag=method.delivery_tag)

def iniciar_worker():
    print("[*] Conectando ao RabbitMQ...")
    # Conecta no RabbitMQ (que está rodando no Docker na localhost)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    # Garante que a fila existe (caso o worker inicie antes da API)
    channel.queue_declare(queue='logs_queue')

    # Diz ao canal para usar a função 'processar_log' sempre que chegar mensagem
    channel.basic_consume(queue='logs_queue', on_message_callback=processar_log)

    print("[*] Worker iniciado. Aguardando mensagens na fila 'logs_queue'. Para sair, pressione CTRL+C")
    
    # Inicia o loop infinito escutando a fila
    channel.start_consuming()

if __name__ == '__main__':
    try:
        iniciar_worker()
    except KeyboardInterrupt:
        print("\n[!] Worker interrompido pelo usuário.")
