<?php
// Verifica se os dados foram enviados via POST
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Recebe os dados do formulário
    $data = $_POST['data'];

    // Aqui você pode fazer o que precisa com os dados, como salvá-los em um arquivo ou banco de dados
    $filename = 'dados.txt'; // Nome do arquivo para salvar os dados

    // Abre o arquivo em modo de append (acrescentar)
    $file = fopen($filename, 'a');

    if ($file) {
        fwrite($file, $data . "\n"); // Escreve os dados no arquivo
        fclose($file); // Fecha o arquivo
        echo "Dados registrados com sucesso!";
    } else {
        echo "Erro ao abrir o arquivo.";
    }
} else {
    echo "Método não suportado.";
}
?>