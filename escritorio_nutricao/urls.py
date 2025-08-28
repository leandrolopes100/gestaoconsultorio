from django.contrib import admin
from django.urls import path
from nutri.views import(PacienteList, PacienteUpdate, PacienteCreate, PacienteDetail, PacienteDelete, ConsultaList,
    ConsultaCreate, ConsultaDetail,  ConsultaUpdate, ConsultaDelete, MarcarComoFeita, AvaliacaoCreateView, AvaliacaoDetail,
     AvaliacaoUpdate, AvaliacaoDelete, exportar_avaliacao )
urlpatterns = [
    path('admin/', admin.site.urls),
    path('pacientes/', PacienteList.as_view(), name='pacientes'),
    path('pacientes/adicionar', PacienteCreate.as_view(), name='adicionar_paciente'),
    path('pacientes/<int:pk>/excluir', PacienteDelete.as_view(), name='excluir_paciente'),
    path('pacientes/<int:pk>/editar', PacienteUpdate.as_view(), name='editar_paciente'),
    path('pacientes/<int:pk>/detalhes', PacienteDetail.as_view(), name='detalhes_paciente'),
    #-------CONSULTAS ----------------------
    path('consultas/', ConsultaList.as_view(), name='consultas'),
    path('consultas/adicionar', ConsultaCreate.as_view(), name='adicionar_consulta'),
    path('consultas/<int:pk>/detalhes/', ConsultaDetail.as_view(), name='detalhes_consulta'),
    path('consultas/<int:pk>/excluir/', ConsultaDelete.as_view(), name='excluir_consulta'),
    path('consultas/<int:pk>/editar/', ConsultaUpdate.as_view(), name='editar_consulta'),
    path('consultas/<int:consulta_id>/feita/', MarcarComoFeita.as_view(), name='consulta_feita'),
    #-------CONSULTAS ----------------------
    path('consultas/<int:consulta_id>/avaliacao/criar/', AvaliacaoCreateView.as_view(), name='criar_avaliacao'),
    path('consultas/<int:consulta_id>/avaliacao/detalhes/', AvaliacaoDetail.as_view(), name='detalhes_avaliacao'),
    path('consultas/<int:pk>/avaliacao/editar/', AvaliacaoUpdate.as_view(), name='editar_avaliacao'),
    path('avaliacao/<int:pk>/excluir/', AvaliacaoDelete.as_view(), name='excluir_avaliacao'),
    path('avaliacao/<int:pk>/exportar/', exportar_avaliacao, name='exportar_avaliacao'),

]
