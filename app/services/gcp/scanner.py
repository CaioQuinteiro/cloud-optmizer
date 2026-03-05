import google.auth
from google.cloud import recommender_v1

def obter_vms_ociosas(zona: str):
    """Busca instâncias do Compute Engine ociosas."""
    credentials, project_id = google.auth.default()
    client = recommender_v1.RecommenderClient()
    
    recommender_id = "google.compute.instance.IdleResourceRecommender"
    parent = f"projects/{project_id}/locations/{zona}/recommenders/{recommender_id}"
    
    request = recommender_v1.ListRecommendationsRequest(parent=parent)
    recommendations = client.list_recommendations(request=request)
    
    resultados = []
    economia_total = 0
    
    for rec in recommendations:
        economia = abs(rec.primary_impact.cost_projection.cost.units)
        moeda = rec.primary_impact.cost_projection.cost.currency_code
        economia_total += economia
        
        resultados.append({
            "descricao": rec.description,
            "economia": economia,
            "moeda": moeda,
            "recurso": rec.content.overview.get("resourceName", "Desconhecido")
        })
        
    return {
        "projeto": project_id,
        "zona": zona,
        "oportunidades": len(resultados),
        "economia_total_estimada": economia_total,
        "detalhes": resultados
    }

def obter_discos_ociosos(zona: str):
    """Busca discos rígidos órfãos/ociosos."""
    credentials, project_id = google.auth.default()
    client = recommender_v1.RecommenderClient()
    
    recommender_id = "google.compute.disk.IdleResourceRecommender"
    parent = f"projects/{project_id}/locations/{zona}/recommenders/{recommender_id}"
    
    request = recommender_v1.ListRecommendationsRequest(parent=parent)
    recommendations = client.list_recommendations(request=request)
    
    resultados = []
    economia_total = 0
    
    for rec in recommendations:
        economia = abs(rec.primary_impact.cost_projection.cost.units)
        moeda = rec.primary_impact.cost_projection.cost.currency_code
        economia_total += economia
        
        recurso_bruto = rec.content.overview.get("resourceName", "Desconhecido")
        nome_disco = recurso_bruto.split("disks/")[-1] if "disks/" in recurso_bruto else recurso_bruto
        
        resultados.append({
            "descricao": rec.description,
            "economia": economia,
            "moeda": moeda,
            "disco": nome_disco
        })
        
    return {
        "projeto": project_id,
        "zona": zona,
        "oportunidades": len(resultados),
        "economia_total_estimada": economia_total,
        "detalhes": resultados
    }

def obter_sql_ociosos(zona: str):
    """Busca instâncias do Cloud SQL ociosas."""
    import google.auth
    from google.cloud import recommender_v1
    
    credentials, project_id = google.auth.default()
    client = recommender_v1.RecommenderClient()
    
    # O radar agora aponta para o Cloud SQL
    recommender_id = "google.cloudsql.instance.IdleRecommender"
    parent = f"projects/{project_id}/locations/{zona}/recommenders/{recommender_id}"
    
    request = recommender_v1.ListRecommendationsRequest(parent=parent)
    
    try:
        recommendations = client.list_recommendations(request=request)
    except Exception as e:
        # Retorna vazio caso o Recommender do SQL não esteja ativo na zona/projeto
        print(f"Aviso ao buscar SQL: {e}")
        recommendations = []
    
    resultados = []
    economia_total = 0
    
    for rec in recommendations:
        economia = abs(rec.primary_impact.cost_projection.cost.units)
        moeda = rec.primary_impact.cost_projection.cost.currency_code
        economia_total += economia
        
        recurso_bruto = rec.content.overview.get("resourceName", "Desconhecido")
        nome_instancia = recurso_bruto.split("instances/")[-1] if "instances/" in recurso_bruto else recurso_bruto
        
        resultados.append({
            "descricao": rec.description,
            "economia": economia,
            "moeda": moeda,
            "instancia_sql": nome_instancia
        })
        
    return {
        "projeto": project_id,
        "zona": zona,
        "oportunidades": len(resultados),
        "economia_total_estimada": economia_total,
        "detalhes": resultados
    }