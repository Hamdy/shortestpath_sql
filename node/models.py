from django.db import models

class Node(models.Model):
    name =  models.CharField(max_length=10, unique=True)

class Edge(models.Model):
    start = models.CharField(max_length=10)
    end = models.CharField(max_length=10)

    @staticmethod
    def get_shortestpath(start, end):
        return Edge.objects.raw(
            """
            with recursive cte as (
            select id, start, end, 1 as lev, (start || '->' || end) as path
            from node_edge
            where start = '%s'
            union all
            select e.id, e.start, e.end, lev + 1 , (cte.path || '->' || e.end) as path
            from cte join
                node_edge e
                on e.start = cte.end
            where lev < 100 or e.end = '%s'
            )
            select cte.*
            from cte
            where cte.end = '%s'
            order by lev
            limit 100;
            """ % (start, end, end)
        )

    class Meta:
        unique_together = ('start', 'end')

