#!/usr/bin/env python3
"""
Multimodal RAG System - Main Entry Point
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

def main():
    """Main application entry point"""
    console.print(Panel.fit(
        "[bold blue]Multimodal RAG System[/bold blue]\n"
        "AI Engineering Intern Assignment\n"
        "No-API Version",
        border_style="green"
    ))
    
    # Initialize RAG system
    try:
        from src.core.rag_system import MultimodalRAG
        rag_system = MultimodalRAG()
        console.print("✅ [green]RAG system initialized successfully[/green]")
    except Exception as e:
        console.print(f"❌ [red]Failed to initialize RAG system: {e}[/red]")
        import traceback
        traceback.print_exc()
        return
    
    while True:
        console.print("\n" + "="*50)
        console.print("[bold]Options:[/bold]")
        console.print("1. 📁 Process documents from folder")
        console.print("2. 🔍 Query the system")
        console.print("3. 📊 Show statistics")
        console.print("4. 🎯 Run demo")
        console.print("5. 🚪 Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            process_documents(rag_system)
        elif choice == "2":
            query_system(rag_system)
        elif choice == "3":
            show_statistics(rag_system)
        elif choice == "4":
            run_demo_option()
        elif choice == "5":
            console.print("[yellow]Goodbye! 👋[/yellow]")
            break
        else:
            console.print("[red]Invalid choice. Please try again.[/red]")

def process_documents(rag_system):
    """Process documents from a folder"""
    folder_path = input("Enter folder path (or press Enter for ./data/input): ").strip()
    if not folder_path:
        folder_path = "./data/input"
    
    if not os.path.exists(folder_path):
        console.print(f"[red]Folder not found: {folder_path}[/red]")
        return
    
    console.print(f"[blue]Processing documents from: {folder_path}[/blue]")
    
    try:
        results = rag_system.process_folder(folder_path)
        
        # Display results
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
    """Query the RAG system"""
    query = input("Enter your query: ").strip()
    if not query:
        console.print("[red]Query cannot be empty[/red]")
        return
    
    try:
        top_k_input = input("Enter top_k (default 5): ").strip()
        top_k = int(top_k_input) if top_k_input else 5
        
        threshold_input = input("Enter similarity threshold (default 0.2): ").strip()
        threshold = float(threshold_input) if threshold_input else 0.2
        
        console.print(f"\n[blue]Searching for: '{query}'[/blue]")
        results = rag_system.search(query, top_k=top_k, threshold=threshold)
        
        if not results:
            console.print("[yellow]No relevant results found.[/yellow]")
            return
        
        # Display results
        table = Table(title=f"🔍 Search Results for: '{query}'")
        table.add_column("#", style="cyan")
        table.add_column("Score", style="green")
        table.add_column("Type", style="yellow")
        table.add_column("Source", style="magenta")
        table.add_column("Content Preview", style="white")
        
        for i, result in enumerate(results, 1):
            content_preview = result['content'][:100] + "..." if len(result['content']) > 100 else result['content']
            table.add_row(
                str(i),
                f"{result['score']:.3f}",
                result['document_type'],
                result['metadata'].get('filename', 'Unknown'),
                content_preview
            )
        
        console.print(table)
        
    except ValueError:
        console.print("[red]Invalid input value. Using defaults.[/red]")
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

def run_demo_option():
    """Run the demo from interactive mode"""
    try:
        # Import demo function directly
        from demo import run_demo
        run_demo()
    except Exception as e:
        console.print(f"❌ [red]Error running demo: {e}[/red]")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()