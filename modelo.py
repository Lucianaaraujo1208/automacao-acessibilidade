import tensorflow as tf

def criar_modelo():
    modelo = tf.keras.Sequential([
        tf.keras.layers.Dense(128, activation='relu', input_shape=(10,)),  # Ajuste a forma de entrada
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')  # Saída binária
    ])
    modelo.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return modelo

if __name__ == "__main__":
    modelo = criar_modelo()
    print("Modelo criado com sucesso!")