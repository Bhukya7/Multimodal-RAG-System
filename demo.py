#!/usr/bin/env python3
"""
Improved Demo Script for Multimodal RAG System
"""

import os
import sys
from pathlib import Path
from rich.console import Console
from rich.table import Table

# Add current directory to path to ensure imports work
sys.path.append(str(Path(__file__).parent))

console = Console()

def run_demo():
    """Run a comprehensive demo"""
    console.print("[bold blue]🚀 Starting Multimodal RAG System Demo[/bold blue]")
    
    try:
        from src.core.rag_system import MultimodalRAG
    except ImportError as e:
        console.print(f"❌ [red]Import error: {e}[/red]")
        return
    
    # Initialize RAG system
    try:
        console.print("🔄 Initializing RAG system...")
        rag = MultimodalRAG()
        console.print("✅ [green]RAG system initialized successfully[/green]")
    except Exception as e:
        console.print(f"❌ [red]Failed to initialize RAG system: {e}[/red]")
        import traceback
        traceback.print_exc()
        return
    
    # Create sample data directory structure
    sample_data_dir = Path("./data/input")
    sample_data_dir.mkdir(parents=True, exist_ok=True)
    
    # Create better sample text files with more content
    console.print("\n📝 Creating sample documents...")
    
    # Sample 1: AI Concepts (more detailed)
    ai_content = """
    ARTIFICIAL INTELLIGENCE OVERVIEW

    Artificial Intelligence (AI) refers to the simulation of human intelligence processes by machines, especially computer systems. These processes include learning, reasoning, and self-correction.

    Key applications of AI include:
    - Expert systems
    - Natural language processing (NLP)
    - Speech recognition
    - Machine vision

    AI can be categorized as either weak or strong. Weak AI is designed to perform a narrow task, while strong AI can perform any intellectual task that a human can.

    MACHINE LEARNING FUNDAMENTALS

    Machine Learning is a subset of AI that focuses on building systems that learn from data. Instead of being explicitly programmed, ML models learn patterns from data.

    There are three main types of machine learning:
    1. Supervised Learning - Learning from labeled data
    2. Unsupervised Learning - Finding patterns in unlabeled data  
    3. Reinforcement Learning - Learning through trial and error

    DEEP LEARNING ADVANCEMENTS

    Deep Learning uses neural networks with many layers to learn from large amounts of data. These deep neural networks have revolutionized fields like computer vision and natural language processing.

    Popular deep learning architectures include:
    - Convolutional Neural Networks (CNNs) for images
    - Recurrent Neural Networks (RNNs) for sequences
    - Transformers for natural language processing

    The transformer architecture, introduced in 2017, has become the foundation for modern large language models like GPT and BERT.
    """
    
    with open(sample_data_dir / "ai_ml_dl.txt", "w", encoding="utf-8") as f:
        f.write(ai_content)
    
    # Sample 2: Sales Report (more detailed)
    sales_content = """
    QUARTERLY SALES REPORT - Q4 2024

    EXECUTIVE SUMMARY:
    Total revenue for Q4 2024 reached $3.59 million, representing a 15% increase compared to Q3 2024. This growth was driven by strong performance across all product lines and geographic regions.

    PRODUCT PERFORMANCE:

    Product A: Next-Gen Smartphone
    - Revenue: $1.2 million
    - Units sold: 8,000
    - Growth: +12% quarter-over-quarter
    - Key markets: North America, Europe

    Product B: Enterprise Software Suite  
    - Revenue: $890,000
    - Units sold: 445 licenses
    - Growth: +18% quarter-over-quarter
    - Key markets: Global enterprise clients

    Product C: AI Analytics Platform
    - Revenue: $1.5 million
    - Units sold: 150 enterprise contracts
    - Growth: +25% quarter-over-quarter
    - Key markets: Technology, Finance sectors

    REGIONAL BREAKDOWN:

    North America:
    - Total revenue: $2.1 million
    - Growth: +14% from previous quarter
    - Top product: Product C (AI Analytics)

    Europe:
    - Total revenue: $980,000  
    - Growth: +16% from previous quarter
    - Top product: Product A (Smartphone)

    Asia:
    - Total revenue: $510,000
    - Growth: +20% from previous quarter
    - Top product: Product B (Software)

    KEY METRICS:
    - Customer acquisition cost: $1,200
    - Customer lifetime value: $15,800
    - Net promoter score: 68
    - Market share: 22% (up from 19% in Q3)

    The charts in the appendix show detailed growth trajectories for each product category and regional market. Overall, we expect this positive trend to continue into Q1 2025.
    """
    
    with open(sample_data_dir / "sales_report_2024_q4.txt", "w", encoding="utf-8") as f:
        f.write(sales_content)
    
    console.print("✅ [green]Created detailed sample documents[/green]")
    
    # Process documents
    console.print("\n[bold]📁 Processing sample documents...[/bold]")
    try:
        results = rag.process_folder(str(sample_data_dir))
        console.print("✅ Document processing completed")
    except Exception as e:
        console.print(f"❌ [red]Error processing documents: {e}[/red]")
        import traceback
        traceback.print_exc()
        return
    
    # Display processing results
    table = Table(title="Processing Results")
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
    
    # Wait a moment for processing to complete
    import time
    time.sleep(2)
    
    # Better demo queries that match the content
    demo_queries = [
        "What is artificial intelligence?",
        "Explain machine learning types",
        "Tell me about deep learning",
        "Sales revenue for Q4 2024",
        "Which product had highest revenue?",
        "North America sales performance",
        "What are neural networks?",
        "Customer acquisition cost"
    ]
    
    console.print("\n[bold]🔍 Running demo queries...[/bold]")
    
    successful_searches = 0
    for query in demo_queries:
        console.print(f"\n[cyan]Query: {query}[/cyan]")
        try:
            # Use lower threshold for demo
            results = rag.search(query, top_k=3, threshold=0.2)
            
            if results:
                successful_searches += 1
                for i, result in enumerate(results, 1):
                    score = result['score']
                    doc_type = result['document_type']
                    source = result['metadata'].get('filename', 'Unknown')
                    preview = result['content'][:100] + "..." if len(result['content']) > 100 else result['content']
                    
                    console.print(f"  {i}. [{doc_type}] {score:.3f} - {source}")
                    console.print(f"     {preview}")
            else:
                console.print("  [yellow]No results found[/yellow]")
        except Exception as e:
            console.print(f"  [red]Error during query: {e}[/red]")
    
    # Show statistics
    console.print("\n[bold]📊 System Statistics:[/bold]")
    try:
        stats = rag.get_stats()
        console.print(f"  Total documents: {stats['total_documents']}")
        console.print(f"  Embedding model: {stats['embedding_model']}")
        console.print(f"  Collection: {stats['collection_name']}")
        console.print(f"  Successful searches: {successful_searches}/{len(demo_queries)}")
    except Exception as e:
        console.print(f"  [red]Error getting statistics: {e}[/red]")
    
    if successful_searches > 0:
        console.print("\n🎉 [bold green]Demo completed successfully![/bold green]")
    else:
        console.print("\n⚠️ [bold yellow]Demo ran but no search results found. Check similarity threshold.[/bold yellow]")
    
    console.print("\n💡 [bold]Try the interactive mode:[/bold] python src/main.py")

if __name__ == "__main__":
    run_demo()