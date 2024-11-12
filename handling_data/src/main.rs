use actix_web::{post, web, App, HttpServer, Responder, HttpResponse};
use serde::{Deserialize, Serialize};
use serde_json::json;

#[derive(Debug, Serialize, Deserialize, Clone)]
struct FileMetadata {
    filename: String,
    content_type: String,
    description: String,
}

#[post("/process_metadata")]
async fn process_metadata(metadata: web::Json<FileMetadata>) -> impl Responder {
    // Display received metadata in console
    println!("Received metadata: {:?}", metadata);

    // Send success response
    HttpResponse::Ok().json(json!({
        "status": "Metadata processed successfully",
        "filename": metadata.filename.clone()
    }))
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    println!("Server starting at http://127.0.0.1:8080");
    
    HttpServer::new(|| {
        App::new()
            .wrap(actix_web::middleware::Logger::default())
            .service(process_metadata)
    })
    .bind("127.0.0.1:8080")?
    .run()
    .await
}