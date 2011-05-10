"""
Signals for dataset related events.  All _pre_ handlers should a boolean value
that is used to determine whether or not the operation should be executed.  If
False is returned, the corresponding Response will be a HttpResponseBadRequest.

 - `dataset_pre_create`: sent before creation of a new dataset
        Ex: responses = dataset_pre_create.send(Sender, user=User)

 - `dataset_create`: sent on creation of a new dataset
        Ex: dataset_create.send(Sender, dataset=DataProfile)

 - `dataset_pre_update_profile`: sent before update of a dataset profile
        Ex: responses = dataset_pre_update_profile.send(Sender, 
                                                        dataset=DataProfile)

 - `dataset_update_profile`: sent on update of a dataset profile
        Ex: dataset_update_profile.send(Sender, dataset=DataProfile)

 - `dataset_pre_update_datafile`: sent before update of a data file
        Ex: responses = dataset_update_datafile.send(Sender, datafile=DataFile) 

 - `dataset_update_datafile`: sent on update of a data file
        Ex: dataset_update_datafile.send(Sender, datafile=DataFile) 

 - `dataset_pre_delete`: sent before a dataset is deleted
        Ex: responses = dataset_delete.send(Sender, dataset=DataProfile)

 - `dataset_delete`: sent when a dataset is deleted
        Ex: dataset_delete.send(Sender, dataset=DataProfile)

 - `dataset_pre_render`: sent before the pager view for a dataset is rendered
        Ex: responses = dataset_pre_render.send(Sender, 
                                                request=request,
                                                dataset=DataProfile)

 - `dataset_render`: sent when the pager view for a dataset is rendered
        Ex: dataset_render.send(Sender, 
                                request=request,
                                dataset=DataProfile)

 - `dataset_editor_pre_render`: sent before rendering the dataset editor view
        Ex: responses = dataset_editor_pre_render.send(Sender, 
                                                request=request,
                                                dataset=DataProfile)

 - `dataset_editor_render`: sent when rendering the dataset editor view
        Ex: dataset_editor_render.send(Sender, 
                                       request=request,
                                       dataset=DataProfile)

 - `dataset_upload_pre_render`: sent before rendering the dataset upload view
        Ex: responses = dataset_pre_render.send(Sender, 
                                                request=request,
                                                username=username)

 - `dataset_upload_render`: sent when rendering the dataset upload view
         Ex: dataset_pre_render.send(Sender, 
                                    request=request,
                                    username=username)

"""
import django.dispatch


dataset_pre_create = django.dispatch.Signal()
dataset_create = django.dispatch.Signal()

dataset_pre_update_profile = django.dispatch.Signal()
dataset_update_profile = django.dispatch.Signal()

dataset_pre_update_datafile= django.dispatch.Signal()
dataset_update_datafile = django.dispatch.Signal()

dataset_pre_delete = django.dispatch.Signal()
dataset_delete = django.dispatch.Signal()

dataset_pre_render = django.dispatch.Signal()
dataset_render = django.dispatch.Signal()

dataset_editor_pre_render = django.dispatch.Signal()
dataset_editor_render = django.dispatch.Signal()

dataset_upload_pre_render = django.dispatch.Signal()
dataset_upload_render = django.dispatch.Signal()

