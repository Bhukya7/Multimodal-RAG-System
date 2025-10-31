"""
Fixed Interactive Mode - No Formatting Errors
"""

import os
import sys
from pathlib import Path

current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from src.core.rag_system import MultimodalRAG

console = Console()

def main():
    """Main application entry point"""
    console.print(Panel.fit(
        "[bold blue]🚀 Multimodal RAG System[/bold blue]\n"
        "AI Engineering Intern Assignment - WORKING VERSION\n"
        "No-API Version",
        border_style="green"
    ))
    
    try:
        rag_system = MultimodalRAG()
        console.print("✅ [green]RAG system initialized successfully[/green]")
        
        stats = rag_system.get_stats()
        console.print(f"📊 [blue]Documents in database: {stats['total_documents']}[/blue]")
        
    except Exception as e:
        console.print(f"❌ [red]Failed to initialize RAG system: {e}[/red]")
        return
    
    while True:
        console.print("\n" + "="*60)
        console.print("[bold]🎯 OPTIONS:[/bold]")
        console.print("1. 📁 Process documents from folder")
        console.print("2. 🔍 Query the system (recommended: threshold 0.1-0.2)")
        console.print("3. 📊 Show statistics") 
        console.print("4. 🎯 Run full demo")
        console.print("5. 🚪 Exit")
        console.print("="*60)
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            process_documents(rag_system)
        elif choice == "2":
            query_system(rag_system)
        elif choice == "3":
            show_statistics(rag_system)
        elif choice == "4":
            run_demo_option(rag_system)
        elif choice == "5":
            console.print("[yellow]👋 Goodbye![/yellow]")
            break
        else:
            console.print("[red]❌ Invalid choice. Please try again.[/red]")

def process_documents(rag_system):
    """Process documents from a folder"""
    folder_path = input("Enter folder path (or press Enter for ./data/input): ").strip()
    if not folder_path:
        folder_path = "./data/input"
    
    if not os.path.exists(folder_path):
        console.print(f"[red]❌ Folder not found: {folder_path}[/red]")
        return
    
    console.print(f"[blue]📁 Processing documents from: {folder_path}[/blue]")
    
    try:
        results = rag_system.process_folder(folder_path)
        
        table = Table(title="📊 Processing Results")
        table.add_column("File Type", style="cyan")
        table.add_column("Files Processed", style="green")
        table.add_column("Chunks Created", style="yellow")
        
        for file_type, stats in results.items():
            if file_type not in ["total_files", "total_chunks"]:
                table.add_row(
                    file_type,
                    str(stats['files_processed']),
                    str(stats['chunks_created'])
                )
        
        console.print(table)
        console.print(f"📊 [green]Total: {results['total_files']} files, {results['total_chunks']} chunks[/green]")
        console.print("✅ [green]Processing completed![/green]")
        
    except Exception as e:
        console.print(f"❌ [red]Error processing documents: {e}[/red]")

def query_system(rag_system):
    """Query the RAG system with better defaults"""
    query = input("Enter your query: ").strip()
    if not query:
        console.print("[red]❌ Query cannot be empty[/red]")
        return
    
    try:
        top_k_input = input("Enter top_k (default 5): ").strip()
        top_k = int(top_k_input) if top_k_input else 5
        
        threshold_input = input("Enter similarity threshold (default 0.2): ").strip()
        threshold = float(threshold_input) if threshold_input else 0.2
        
        console.print(f"\n[blue]🔍 Searching for: '{query}'[/blue]")
        console.print(f"[dim]Using threshold: {threshold}[/dim]")
        
        results = rag_system.search(query, top_k=top_k, threshold=threshold)
        
        if not results:
            console.print("[yellow]⚠️ No relevant results found.[/yellow]")
            console.print("[dim]💡 Try lowering the similarity threshold to 0.1[/dim]")
            return
        
        table = Table(title=f"🎯 Search Results for: '{query}'")
        table.add_column("#", style="cyan")
        table.add_column("Score", style="green")
        table.add_column("Type", style="yellow")
        table.add_column("Source", style="magenta")
        table.add_column("Content Preview", style="white")
        
        for i, result in enumerate(results, 1):
            content_preview = result['content'][:80] + "..." if len(result['content']) > 80 else result['content']
            score_color = "green" if result['score'] > 0.5 else "yellow" if result['score'] > 0.3 else "red"
            table.add_row(
                str(i),
                f"[{score_color}]{result['score']:.3f}[/{score_color}]",
                result['document_type'],
                result['metadata'].get('filename', 'Unknown'),
                content_preview
            )
        
        console.print(table)
        
        if results[0]['score'] < 0.3:
            console.print("\n[dim]💡 Tip: For better results, try:[/dim]")
            console.print("[dim]   - Lower threshold to 0.1[/dim]")
            console.print("[dim]   - Use more specific queries[/dim]")
            console.print("[dim]   - Add more relevant documents[/dim]")
        
    except Exception as e:
        console.print(f"❌ [red]Error during query: {e}[/red]")

def show_statistics(rag_system):
    """Show system statistics"""
    try:
        stats = rag_system.get_stats()
        
        table = Table(title="📊 System Statistics")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Total Documents", str(stats['total_documents']))
        table.add_row("Document Types", ", ".join(stats['document_types']))
        table.add_row("Collection Name", stats['collection_name'])
        table.add_row("Embedding Model", stats['embedding_model'])
        
        console.print(table)
        
    except Exception as e:
        console.print(f"❌ [red]Error getting statistics: {e}[/red]")

def run_demo_option(rag_system):
    """Run the demo from interactive mode"""
    try:
        from demo import run_demo
        run_demo()
    except Exception as e:
        console.print(f"❌ [red]Error running demo: {e}[/red]")

if __name__ == "__main__":
    main()