use reqwest;
use std::fs::File;
use std::io::{Read, Write};
use std::thread;
use std::time::Duration;
use std::sync::{Arc, Mutex};

// Создали словарик для того, чтобы использовать его в download_file
// Решение вызвано тем, что возвращаются разные ошибки в функции std::io::Error и reqwest::Error
// std::io::Error - встречается при попытке записи байтов в файл
// 
#[derive(Debug)]
enum CustomError {
    Io(std::io::Error),
    Reqwest(reqwest::Error),
}

impl From<std::io::Error> for CustomError {
    fn from(err: std::io::Error) -> CustomError {
        CustomError::Io(err)
    }
}

impl From<reqwest::Error> for CustomError {
    fn from(err: reqwest::Error) -> CustomError {
        CustomError::Reqwest(err)
    }
}

fn download_file(url: &str, downloaded: Arc<Mutex<u64>>) -> Result<(), CustomError> {
    let mut response = reqwest::blocking::get(url)?;

    let content_length = response.content_length();
    let mut buffer = [0; 4096];
    let mut downloaded_bytes = 0;

    let filename = "test.txt";

    // Открываем файл для записи байтов
    let mut file = File::create(filename)?;

    loop {
        match response.read(&mut buffer) {
            Ok(n) if n > 0 => {
                let mut downloaded = downloaded.lock().unwrap();
                *downloaded += n as u64;
                downloaded_bytes += n as u64;

                // Записываем байты в файл
                if let Err(e) = file.write_all(&buffer[0..n]) {
                    return Err(CustomError::Io(e));
                }

                // Выводим прогресс прямо в основном потоке
                if let Some(total) = content_length {
                    println!("Загружено {} из {} байт", downloaded_bytes, total);
                } else {
                    println!("Загружено {} байт", downloaded_bytes);
                }
            }
            Ok(_) => break, // Завершаем цикл при достижении конца файла
            Err(_) => print!("Произошла ошибка") 
        }

        // Добавим небольшую задержку для управления частотой обновлений прогресса
        thread::sleep(Duration::from_millis(100));
    }

    // Выводим сообщение о завершении загрузки
    if let Some(total) = content_length {
        println!("Загрузка файла завершена! Загружено {} из {} байт в файл {}", downloaded_bytes, total, filename);
    } else {
        println!("Загрузка файла завершена! Загружено {} байт в файл {}", downloaded_bytes, filename);
    }

    Ok(())
}

fn main() {
    let url = "https://drive.google.com/uc?export=download&confirm=no_antivirus&id=1B8wQGgNmF4xlbDtQYgN6Lt1SOR8dmgX3";
    let downloaded = Arc::new(Mutex::new(0));

    // Запускаем отдельный поток для отслеживания прогресса
    let downloaded_clone = downloaded.clone();

    thread::spawn(move || {
        loop {
            thread::sleep(Duration::from_secs(1));
            let downloaded = *downloaded_clone.lock().unwrap();
            println!("Прогресс в отдельном потоке: {} байт", downloaded);
        }
    });

    if let Err(e) = download_file(url, downloaded) {
        println!("Произошла ошибка при загрузке файла: {:?}", e);
    }
}