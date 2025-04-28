// Função assíncrona para carregar os dados de um arquivo JSON
async function carregarDados() {
     // Faz uma requisição para buscar o arquivo JSON com os dados de acessibilidade
    const response = await fetch('dados_acessibilidade.json'); // Verifique o caminho correto
    // Converte a resposta da requisição para um objeto JavaScript
    const dados = await response.json();
    return dados;   // Retorna os dados carregados

    // Função carregarDados: Esta função carrega dados de um arquivo JSON que contém informações sobre acessibilidade. Ela utiliza a função fetch para buscar o arquivo e, em seguida, converte a resposta em um objeto JavaScript usando response.json(). O uso do async/await permite que a função trate as operações assíncronas de maneira mais clara.
}

// Função para preparar os dados extraídos do JSON
function prepararDados(dados) {
    // Mapeia os dados para criar um array contendo apenas as descrições
    const descricoes = dados.map(item => item.descricao);
    // Mapeia os dados para criar um array contendo apenas as soluções
    const solucoes = dados.map(item => item.solucao);
    return { descricoes, solucoes }; // Retorna um objeto com descrições e soluções

    // Função prepararDados: Esta função recebe os dados carregados e extrai duas propriedades de cada item: descricao e solucao. Os dados são retornados como um objeto contendo dois arrays: um para as descrições e outro para as soluções. Isso é útil para organizar os dados antes de alimentar o modelo de machine learning.
}

// Função assíncrona para treinar o modelo de machine learning
async function treinarModelo() {
    // Atualiza o status na interface do usuário
    document.getElementById("status").innerText = "Treinando modelo..."; 
     // Carrega os dados utilizando a função carregarDados
    const dados = await carregarDados();
     // Prepara os dados, extraindo descrições e soluções
    const { descricoes, solucoes } = prepararDados(dados);
    // Função treinarModelo: Esta função gerencia o treinamento do modelo. Ela atualiza o status na interface do usuário para indicar que o modelo está sendo treinado, carrega os dados, e prepara as descrições e soluções.

    const modelo = tf.sequential();
    modelo.add(tf.layers.dense({ units: 32, activation: 'relu', inputShape: [1] }));
    modelo.add(tf.layers.dense({ units: 1, activation: 'sigmoid' }));
    // Criação do Modelo: Aqui, um modelo sequencial do TensorFlow.js é criado. O modelo tem duas camadas densas (fully connected layers):
    //A primeira camada tem 32 neurônios e usa a função de ativação ReLU.
    //A segunda camada tem 1 neurônio com ativação sigmoide, o que é comum em problemas de classificação binária.

    // Compila o modelo definindo otimizador e função de perda
    modelo.compile({ optimizer: 'adam', loss: 'binaryCrossentropy', metrics: ['accuracy'] });
    //Compilação do Modelo: O modelo é compilado com o otimizador Adam e a função de perda binaryCrossentropy, adequada para problemas de classificação binária. A métrica de precisão (accuracy) é definida para monitorar o desempenho do modelo durante o treinamento.

    // Prepara os tensores de entrada (comprimento das descrições) e saída (comprimento das soluções)
    const x = tf.tensor2d(descricoes.map(d => d.length), [descricoes.length, 1]);
    const y = tf.tensor2d(solucoes.map(s => s.length), [solucoes.length, 1]);
    //Preparação dos Tensores: Os dados de entrada (x) e os dados de saída (y) são preparados como tensores. Aqui, a entrada é o comprimento das descrições e a saída é o comprimento das soluções, o que pode não ser a abordagem ideal, pois pode não capturar a relação entre as descrições e soluções de forma adequada. Uma abordagem mais avançada poderia usar representações vetoriais (embeddings) ou texto codificado.

    // Inicia o treinamento do modelo
    await modelo.fit(x, y, {
        epochs: 100,
        callbacks: {
            onEpochEnd: async (epoch, logs) => {
                // Atualiza a barra de progresso e o texto de status
                const progress = Math.floor(((epoch + 1) / 100) * 100); 
                document.getElementById("progress-bar").style.width = `${progress}%`; // Corrigido o uso de crase
                document.getElementById("status").innerText = `Treinando modelo... (${progress}%)`; // Corrigido o uso de crase
                console.log(`Epoch ${epoch + 1}: loss = ${logs.loss}`); // Corrigido o uso de crase
            }
        }
       // Treinamento do Modelo: O modelo é treinado com os dados de entrada e saída por 100 épocas. Durante o treinamento, um callback onEpochEnd é usado para atualizar a interface do usuário com o progresso, incluindo uma barra de progresso e mensagens no status.
    });

    // Mensagem de sucesso após o treinamento
    console.log("Modelo treinado com sucesso.");
    document.getElementById("status").innerText = "Modelo treinado com sucesso!"; // Atualiza o status final
    return modelo; // Retorna o modelo treinado
    //Conclusão do Treinamento: Após o treinamento, uma mensagem de sucesso é registrada no console e na interface do usuário.
}

// Função assíncrona para prever a solução com base em uma descrição de erro
async function preverSolucao(modelo, descricaoErro) {
     // Cria um tensor de entrada com o comprimento da descrição do erro
    const tensorEntrada = tf.tensor2d([descricaoErro.length], [1, 1]);
     // Faz a previsão utilizando o modelo
    const previsao = modelo.predict(tensorEntrada);
    // Converte a previsão em um array para fácil manipulação
    const solution = await previsao.arraySync();
     // Loga a solução prevista no console
    console.log(`Solução prevista para '${descricaoErro}': ${solution}`); // Corrigido o uso de crase
    return solution; // Retorna a solução prevista
    // Função preverSolucao: Esta função recebe o modelo treinado e uma descrição de erro para prever a solução. Ela cria um tensor de entrada baseado no comprimento da descrição do erro e usa o modelo para prever a solução correspondente.
}

// Função que é chamada quando o documento HTML é completamente carregado
document.addEventListener('DOMContentLoaded', async () => {
    // Array com as descrições de problemas de acessibilidade a serem analisados
    const issues = [
        "Ensures every id attribute value of active elements is unique",
        // descrições de erros
    ];
     // Treina o modelo e espera a conclusão
    const modelo = await treinarModelo();

    // Para cada problema de acessibilidade, prevê a solução
    for (const issue of issues) {
         // Atualiza o status na interface do usuário durante a análise
        document.getElementById("status").innerText = "Analisando..."; 
        // Chama a função para prever a solução para o problema atual
        const solution = await preverSolucao(modelo, issue);
        // Adiciona o resultado da previsão à interface do usuário
        document.getElementById("resultados").innerHTML += `<p>${issue}: ${solution}</p>`; // Corrigido o uso de crase
    }

    // Mensagem final após a conclusão da análise
    document.getElementById("status").innerText = "Análise concluída."; // Atualiza o status final

    // Execução do Código: Esta parte do código é executada quando o documento HTML é carregado. Ele define uma lista de problemas de acessibilidade, treina o modelo, e para cada problema na lista, prevê a solução correspondente, atualizando a interface do usuário com os resultados.
});