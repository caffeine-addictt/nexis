use axum::{response::Html, routing::get, Router};
use tokio::net::TcpListener;

#[tokio::main]
async fn main() {
    let routes = Router::new().route("/", get(|| async { Html("Test route page") }));

    // Start server
    let listener = TcpListener::bind("127.0.0.1:3000").await.unwrap();
    println!("->> Listening on {:?}\n", listener.local_addr());

    axum::serve(listener, routes.into_make_service())
        .await
        .unwrap();
}
